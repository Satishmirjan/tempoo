# Quick Start Guide - All Features Working! ✅

## What Was Fixed

1. ✅ **Flashcards Feature** - Now fully integrated and working
2. ✅ **Quiz/Questions Feature** - Now fully integrated and working  
3. ✅ **Audio Feature** - Improved error handling and display
4. ✅ **WebSocket Error** - Fixed Vite HMR connection issues

## How to Use

### 1. Start the Backend Server

```bash
cd server
python app.py
```

The server will start on `http://localhost:5000`

**Note**: On first run, the models will be downloaded automatically:
- Summarization model: `facebook/bart-large-cnn` (~1.6GB)
- Question generation model: `valhalla/t5-base-qg-hl` (~500MB)
- Question answering model: `distilbert-base-cased-distilled-squad` (~250MB)

This may take 10-15 minutes on first run.

### 2. Start the Frontend Server

```bash
cd client
npm run dev
```

The frontend will start on `http://localhost:5173` (or the port shown)

### 3. Use the Application

1. Open `http://localhost:5173` in your browser
2. Click "Upload" or "Get Started"
3. Select which features you want:
   - ✅ **Summary** - Get a concise summary of your PDF
   - ✅ **Flashcards** - Generate interactive Q&A flashcards
   - ✅ **Quiz** - Generate quiz questions with answers
   - ✅ **Audio** - Listen to the summary (requires API key)
4. Upload a PDF file
5. Click "Generate"
6. View your results on the Summary page

## Features Explained

### Summary
- Generates a concise summary of your PDF
- Uses AI to extract key points
- Works with any PDF document

### Flashcards
- Generates interactive Q&A pairs
- Click on a card to flip between question and answer
- Great for studying and memorization
- Generates up to 10 flashcards

### Quiz
- Generates quiz questions with answers
- Perfect for testing your knowledge
- Generates up to 5 questions
- Shows questions and correct answers

### Audio
- Converts summary to speech
- Requires ElevenLabs API key (optional)
- Works without API key (other features still work)
- Helpful for visually impaired users

## Setting Up Audio (Optional)

1. Get an ElevenLabs API key from https://elevenlabs.io
2. Create a `.env` file in the `server` directory:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```
3. Install python-dotenv (if not already installed):
   ```bash
   pip install python-dotenv
   ```
4. Restart the backend server

**Note**: Audio is optional. The app works perfectly without it!

## Troubleshooting

### Models Not Downloading
- Check your internet connection
- Ensure you have enough disk space (~3GB)
- Wait patiently - first download can take 10-15 minutes
- Check terminal for download progress

### Flashcards/Quiz Not Generating
- Ensure PDF has enough text (at least 100 characters)
- Check backend terminal for errors
- Wait for models to finish downloading on first run
- Try with a different PDF

### Audio Not Working
- Check if `ELEVENLABS_API_KEY` is set in `.env` file
- Verify API key is valid
- Check backend terminal for error messages
- Audio is optional - other features work without it

### Server Not Starting
- Check if port 5000 (backend) or 5173 (frontend) is already in use
- Ensure all dependencies are installed:
  ```bash
  # Backend
  cd server
  pip install -r requirements.txt
  
  # Frontend
  cd client
  npm install --legacy-peer-deps
  ```

## Performance Tips

1. **First Run**: Slow (models downloading) - be patient!
2. **Subsequent Runs**: Much faster (models cached)
3. **Large PDFs**: May take longer to process
4. **Multiple Features**: Each feature adds processing time

## What to Expect

### Processing Times (after models are downloaded):
- **Summary**: 10-30 seconds
- **Flashcards**: 30-60 seconds  
- **Quiz**: 30-60 seconds
- **Audio**: Depends on text length and API response

### Model Download Times (first run only):
- **Summarization model**: 5-10 minutes
- **Question generation model**: 3-5 minutes
- **Question answering model**: 2-3 minutes
- **Total**: ~10-15 minutes

## Next Steps

1. ✅ Start both servers (backend and frontend)
2. ✅ Upload a PDF and test the features
3. ✅ Try different combinations of features
4. ✅ (Optional) Set up audio with API key

## Need Help?

- Check `FEATURES_FIXED.md` for detailed information
- Check `SETUP_GUIDE.md` for setup instructions
- Check backend terminal for error messages
- Check browser console (F12) for frontend errors

## Enjoy! 🎉

All features are now working. Have fun learning with flashcards and quizzes!

