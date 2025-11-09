# Setup Guide - LearnAI Application

## Issues Fixed

1. **Frontend npm install issue**: Fixed by using `--legacy-peer-deps` flag
2. **VoiceAssistant browser compatibility**: Added better error handling and browser support checks
3. **TTS API key handling**: Made TTS optional when API key is not set, with graceful error handling
4. **Server error handling**: Improved error handling for audio generation failures

## Quick Start

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8 or higher
- npm or yarn

### Frontend Setup

1. Navigate to the client directory:
```bash
cd client
```

2. Install dependencies:
```bash
npm install --legacy-peer-deps
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (or the port shown in terminal)

### Backend Setup

1. Navigate to the server directory:
```bash
cd server
```

2. Install Python dependencies (recommended: use a virtual environment):
```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python app.py
```

The backend will be available at `http://localhost:5000`

**Note**: On first run, the backend will download the BART summarization model (~1.6GB). This may take several minutes depending on your internet connection.

### Optional: Text-to-Speech Setup

If you want to use the TTS feature:

1. Get an ElevenLabs API key from https://elevenlabs.io
2. Create a `.env` file in the `server` directory:
```
ELEVENLABS_API_KEY=your_api_key_here
```

3. Install python-dotenv (if not already installed):
```bash
pip install python-dotenv
```

**Note**: The application will work without the TTS API key. Audio generation will be skipped if the key is not set.

## Running the Application

1. Start the backend server first (in one terminal):
```bash
cd server
python app.py
```

2. Start the frontend server (in another terminal):
```bash
cd client
npm run dev
```

3. Open your browser and navigate to the frontend URL (usually `http://localhost:5173`)

## Features

- ✅ PDF Upload and Summarization
- ✅ Text-to-Speech (requires API key)
- ✅ Voice Navigation (browser must support speech recognition)
- ✅ Dark Mode Toggle
- ✅ Responsive Design

## Troubleshooting

### Frontend Issues

- **npm install fails**: Use `npm install --legacy-peer-deps`
- **Port already in use**: Change the port in `vite.config.js` or kill the process using the port
- **Voice recognition not working**: Ensure you're using a modern browser (Chrome, Edge) and have granted microphone permissions

### Backend Issues

- **Model download takes time**: This is normal on first run. The BART model is ~1.6GB
- **TTS not working**: Check if ELEVENLABS_API_KEY is set in your `.env` file
- **Port 5000 already in use**: Change the port in `app.py` (line 107) or kill the process using port 5000

### Common Errors

- **"No module named 'flask'"**: Install dependencies with `pip install -r requirements.txt`
- **"Transformers model not found"**: Wait for the model to finish downloading on first run
- **CORS errors**: Ensure the backend is running and CORS is enabled (it should be by default)

## Development

### Frontend Structure
- `src/App.jsx` - Main application component
- `src/components/` - Reusable components
- `src/pages/` - Page components
- `src/components/VoiceAssistant.jsx` - Voice navigation component

### Backend Structure
- `app.py` - Main Flask application
- `tts_model.py` - Text-to-speech generation
- `summarizer.py` - Text summarization utilities

## Notes

- The application requires both frontend and backend to be running simultaneously
- Voice navigation works best in Chrome or Edge browsers
- PDF summarization may take time for large documents
- TTS feature is optional and requires an ElevenLabs API key

