from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import pipeline
import fitz  # PyMuPDF
import os
import tempfile
import json
from tts_model import generate_speech
from flashcard_generator import generate_flashcards, generate_quiz

app = Flask(__name__)
CORS(app)

# Summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Directory to store TTS audio files
AUDIO_OUTPUT_DIR = "tts_chunks"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def split_into_chunks(text, max_words=700):
    words = text.split()
    chunks = []
    current_chunk = []
    count = 0
    for word in words:
        count += 1
        current_chunk.append(word)
        if count >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            count = 0
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def summarize_large_text(text):
    chunks = split_into_chunks(text, max_words=700)
    summaries = []
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=200, min_length=60, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            summaries.append(f"[Error summarizing chunk: {e}]")
    return "\n\n".join(summaries)

@app.route('/summary', methods=['POST'])
def summarize_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    options_json = request.form.get("options")

    try:
        options = json.loads(options_json) if options_json else {}
    except Exception as e:
        return jsonify({'error': f'Invalid options format: {e}'}), 400

    summary_enabled = options.get("summary", False)
    audio_enabled = options.get("audio", False)
    flashcards_enabled = options.get("flashcards", False)
    quiz_enabled = options.get("quiz", False)

    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file_path = tmp.name
        file.save(file_path)
        text = extract_text_from_pdf(file_path)

    os.remove(file_path)

    if not text.strip():
        return jsonify({'error': 'Empty or unreadable PDF'}), 400

    # Generate summary if requested or if flashcards/quiz are needed
    # (flashcards/quiz work better with summarized text)
    if summary_enabled or flashcards_enabled or quiz_enabled:
        final_summary = summarize_large_text(text)
    else:
        final_summary = text

    # Initialize response data
    # Include summary only if explicitly requested (even though it's generated for flashcards/quiz)
    response_data = {
        'summary': final_summary if summary_enabled else None,
        'audio_url': None,
        'flashcards': None,
        'quiz': None
    }

    # Generate audio if requested
    if audio_enabled and final_summary:
        try:
            audio_path = generate_speech(final_summary)
            audio_filename = os.path.basename(audio_path)
            response_data['audio_url'] = f"/audio/{audio_filename}"
        except ValueError as e:
            print(f"Audio generation error (API key not set): {e}")
            print("TTS feature requires ELEVENLABS_API_KEY environment variable. Continuing without audio...")
        except Exception as e:
            print(f"Audio generation error: {e}")
            print("Continuing without audio...")

    # Generate flashcards if requested
    if flashcards_enabled and final_summary:
        try:
            print("Generating flashcards...")
            flashcards = generate_flashcards(final_summary, max_flashcards=10)
            response_data['flashcards'] = flashcards
            print(f"Generated {len(flashcards)} flashcards")
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            import traceback
            traceback.print_exc()
            response_data['flashcards'] = []

    # Generate quiz if requested
    if quiz_enabled and final_summary:
        try:
            print("Generating quiz...")
            quiz = generate_quiz(final_summary, num_questions=5)
            response_data['quiz'] = quiz
            print(f"Generated {len(quiz)} quiz questions")
        except Exception as e:
            print(f"Error generating quiz: {e}")
            import traceback
            traceback.print_exc()
            response_data['quiz'] = []

    return jsonify(response_data), 200

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
