import os
import requests
import time
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer

# Try to import pydub (optional - requires ffmpeg)
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    AudioSegment = None

# Download punkt tokenizer data
try:
    nltk.download('punkt', quiet=True)
except:
    pass

# Try to load environment variables if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

HEADERS = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}

def sent_tokenize(text):
    tokenizer = PunktSentenceTokenizer()
    return tokenizer.tokenize(text)

def split_text(text, max_words=200):
    sentences = sent_tokenize(text)
    chunks = []
    current = ""

    for sentence in sentences:
        if len((current + sentence).split()) <= max_words:
            current += " " + sentence
        else:
            chunks.append(current.strip())
            current = sentence
    if current:
        chunks.append(current.strip())
    return chunks

def combine_audio_files_simple(chunk_paths, output_path):
    """
    Combine MP3 files using simple binary concatenation.
    This works for MP3 files from the same encoder (ElevenLabs) as they use consistent encoding.
    Note: For best quality and reliability, install ffmpeg. This is a fallback method.
    """
    try:
        if not chunk_paths:
            return False
        
        # For single chunk, just copy it
        if len(chunk_paths) == 1:
            import shutil
            shutil.copy2(chunk_paths[0], output_path)
            return True
        
        # For multiple chunks from ElevenLabs, simple concatenation usually works
        # because they use consistent MP3 encoding without complex ID3 tags
        with open(output_path, 'wb') as outfile:
            for chunk_path in chunk_paths:
                if os.path.exists(chunk_path):
                    with open(chunk_path, 'rb') as infile:
                        outfile.write(infile.read())
        return True
    except Exception as e:
        print(f"Warning: Simple audio combination failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_speech(text, output_dir="tts_chunks", output_file="output.mp3"):
    # Check if API key is set
    if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "":
        raise ValueError("ElevenLabs API key is not set. Please set ELEVENLABS_API_KEY environment variable or create a .env file.")
    
    os.makedirs(output_dir, exist_ok=True)
    chunks = split_text(text)
    chunk_paths = []

    print(f"Generating {len(chunks)} audio chunks using ElevenLabs...")

    for i, chunk in enumerate(chunks, 1):
        payload = {
            "text": chunk,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
            if response.status_code == 200:
                chunk_path = os.path.join(output_dir, f"chunk_{i}.mp3")
                with open(chunk_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Saved chunk_{i}.mp3")
                chunk_paths.append(chunk_path)
                time.sleep(0.5)  # Reduced delay
            else:
                error_msg = f"Failed to generate chunk {i}: {response.status_code}"
                if response.status_code == 401:
                    error_msg += " - Invalid API key"
                elif response.status_code == 429:
                    error_msg += " - Rate limit exceeded"
                print(f"❌ {error_msg}")
                raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error generating chunk {i}: {e}")
            raise

    if not chunk_paths:
        raise Exception("No audio chunks were generated")

    final_path = os.path.join(output_dir, output_file)
    
    # Try to combine chunks using pydub (requires ffmpeg)
    if PYDUB_AVAILABLE and len(chunk_paths) > 1:
        try:
            print("Combining audio chunks using pydub...")
            combined = AudioSegment.empty()
            for chunk_path in chunk_paths:
                segment = AudioSegment.from_file(chunk_path, format="mp3")
                combined += segment
            combined.export(final_path, format="mp3")
            print(f"🎧 Final audio saved as {final_path}")
            return final_path
        except Exception as e:
            print(f"Warning: pydub combination failed (ffmpeg may not be installed): {e}")
            print("Falling back to simple binary combination...")
    
    # Fallback: Use simple binary combination or serve first chunk
    if len(chunk_paths) == 1:
        # Only one chunk - just rename it
        if os.path.exists(chunk_paths[0]):
            import shutil
            shutil.copy2(chunk_paths[0], final_path)
            print(f"🎧 Final audio saved as {final_path} (single chunk)")
            return final_path
    else:
        # Multiple chunks - try simple combination
        if combine_audio_files_simple(chunk_paths, final_path):
            print(f"🎧 Final audio saved as {final_path} (simple combination)")
            return final_path
        else:
            # Last resort: serve the first chunk
            print(f"⚠️  Could not combine chunks, serving first chunk only")
            import shutil
            shutil.copy2(chunk_paths[0], final_path)
            return final_path
