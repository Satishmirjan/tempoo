import os
from transformers import pipeline
from difflib import SequenceMatcher

# Try to import tavily (optional - for web search fallback)
try:
    from tavily import TavilyClient
    from dotenv import load_dotenv
    load_dotenv()
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")) if os.getenv("TAVILY_API_KEY") else None
except ImportError:
    tavily = None
    print("Tavily not available - web search fallback disabled")

# Load models (lazy loading)
qg_pipeline = None
qa_pipeline = None

def load_models():
    """Lazy load models to avoid loading them if not needed"""
    global qg_pipeline, qa_pipeline
    if qg_pipeline is None:
        print("Loading question generation model...")
        qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-base-qg-hl")
    if qa_pipeline is None:
        print("Loading question answering model...")
        qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    return qg_pipeline, qa_pipeline

def is_similar(q1, q2, threshold=0.85):
    """Check if two questions are similar"""
    return SequenceMatcher(None, q1.lower(), q2.lower()).ratio() > threshold

def deduplicate_questions(questions):
    """Remove duplicate or very similar questions"""
    unique = []
    for q in questions:
        if not any(is_similar(q, uq) for uq in unique):
            unique.append(q)
    return unique

def get_web_answer_tavily(question):
    """Get answer from web search using Tavily (optional)"""
    if not tavily:
        return None
    try:
        result = tavily.search(query=question, search_depth="advanced", include_answer=True)
        if result and result.get("answer"):
            return result["answer"][:100]  # truncate if long
    except Exception as e:
        print(f"Tavily error: {e}")
    return None

def generate_flashcards(summary_text, max_flashcards=10):
    """Generate flashcards (Q&A pairs) from summary text"""
    try:
        qg_pipeline, qa_pipeline = load_models()
        
        # Ensure we have enough text
        if len(summary_text.strip()) < 100:
            print("Summary text is too short for flashcard generation")
            return []
        
        print(f"Generating flashcards from summary (length: {len(summary_text)} chars)")
        
        # Limit input to avoid token limits (use first 2000 chars)
        text_for_questions = summary_text[:2000] if len(summary_text) > 2000 else summary_text
        
        # Generate questions
        try:
            inputs = f"generate questions: {text_for_questions}"
            outputs = qg_pipeline(
                inputs, 
                max_length=256, 
                do_sample=True, 
                top_k=50, 
                top_p=0.95, 
                num_return_sequences=15
            )
        except Exception as e:
            print(f"Error generating questions: {e}")
            return []

        # Extract questions
        raw_questions = []
        for o in outputs:
            if isinstance(o, dict) and 'generated_text' in o:
                gen_text = o['generated_text']
                if '?' in gen_text:
                    question = gen_text.split("?")[0].strip() + '?'
                    # Filter out very short or invalid questions
                    if len(question) > 10 and len(question) < 200:
                        raw_questions.append(question)
        
        if not raw_questions:
            print("No valid questions generated")
            return []
        
        # Remove duplicates
        unique_questions = deduplicate_questions(raw_questions)[:max_flashcards]
        
        if not unique_questions:
            print("No unique questions after deduplication")
            return []
        
        flashcards = []
        # Use full text for answering (but limit to avoid token issues)
        context_text = summary_text[:3000] if len(summary_text) > 3000 else summary_text
        
        for question in unique_questions:
            try:
                # Try to get answer from context
                result = qa_pipeline(question=question, context=context_text)
                answer = result.get('answer', '').strip() if isinstance(result, dict) else str(result).strip()

                # Validate answer
                if not answer or len(answer) < 5 or answer.lower() == question.lower():
                    # Try web search if available
                    web_answer = get_web_answer_tavily(question)
                    if web_answer:
                        answer = web_answer
                    else:
                        # Fallback: extract relevant sentence from summary
                        sentences = summary_text.split('.')
                        for sentence in sentences:
                            sentence = sentence.strip()
                            if len(sentence) > 10:
                                # Check if sentence contains words from question
                                question_words = [w.lower() for w in question.split()[:5] if len(w) > 3]
                                if any(word in sentence.lower() for word in question_words):
                                    answer = sentence[:150]
                                    break
                        if not answer or len(answer) < 5:
                            continue  # Skip this question if no good answer

                # Clean and truncate answer
                answer = answer.replace('\n', ' ').strip()
                if len(answer.split()) > 25:
                    answer = ' '.join(answer.split()[:25]) + '...'

                flashcards.append({
                    "question": question,
                    "answer": answer
                })
            except Exception as e:
                print(f"Error processing question '{question}': {e}")
                continue

        print(f"Successfully generated {len(flashcards)} flashcards")
        return flashcards
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        import traceback
        traceback.print_exc()
        return []

def generate_quiz(summary_text, num_questions=5):
    """Generate quiz questions from summary text (same as flashcards but different format)"""
    flashcards = generate_flashcards(summary_text, max_flashcards=num_questions)
    
    # Convert flashcards to quiz format
    quiz = []
    for i, card in enumerate(flashcards, 1):
        quiz.append({
            "id": i,
            "question": card["question"],
            "correct_answer": card["answer"],
            "options": [card["answer"]]  # Simple format - can be enhanced with distractors
        })
    
    return quiz

