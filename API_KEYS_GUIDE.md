# API Keys Guide - What You Actually Need

## ✅ Required API Keys

### **None!**

All core features work **without any API keys**:

- ✅ **Summary** - Works without API keys
- ✅ **Flashcards** - Works without API keys
- ✅ **Quiz/Questions** - Works without API keys

## 🔑 Optional API Keys

### ElevenLabs API Key (Only for Audio)

**Required for**: Audio/Text-to-Speech feature only

**How to get it**:

1. Go to https://elevenlabs.io
2. Sign up for a free account
3. Get your API key from the dashboard
4. Create a `.env` file in the `server` directory:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```

**What happens without it**:

- Audio feature won't work
- You'll see a helpful error message
- All other features (summary, flashcards, quiz) continue to work perfectly

### Tavily API Key (Optional - Not Required)

**What it's for**: Web search fallback for flashcards (if answers can't be found in the PDF)

**Status**: Not required! The flashcard generator works perfectly without it.

**What happens without it**:

- Flashcards still generate correctly
- Answers are extracted from the PDF content
- No web search fallback (but this is rarely needed)

## Summary

| Feature    | API Key Required?   | Status      |
| ---------- | ------------------- | ----------- |
| Summary    | ❌ No               | ✅ Works    |
| Flashcards | ❌ No               | ✅ Works    |
| Quiz       | ❌ No               | ✅ Works    |
| Audio      | ✅ Yes (ElevenLabs) | ⚠️ Optional |

## What Your Terminal Shows

Looking at your terminal output:

- ✅ **Flashcards**: Working perfectly ("Successfully generated 10 flashcards")
- ✅ **Quiz**: Working perfectly ("Generated 5 quiz questions")
- ⚠️ **Audio**: Needs API key ("Audio generation error (API key not set)")

## Bottom Line

**You ONLY need the ElevenLabs API key if you want audio functionality.**

Everything else works perfectly without any API keys!

## Setting Up Audio (If You Want It)

### Step 1: Create API Key with Correct Permissions

1. Go to https://elevenlabs.io/app/developers/api-keys
2. Click "+ Create Key"
3. **Set Permissions:**
   - ✅ **Text to Speech: Access** (or **Voice Generation: Access**)
   - ❌ **Everything else: No Access**
4. Click "Create Key"
5. **Copy the key immediately** (you won't see it again!)

### Step 2: Add to Project

1. Create `.env` file in `server` directory:
   ```
   ELEVENLABS_API_KEY=your_key_here
   ```
2. Install python-dotenv (if not already installed):
   ```bash
   pip install python-dotenv
   ```
3. Restart the backend server

### Required Permission Only

**You ONLY need:**

- ✅ **Text to Speech: Access** (or **Voice Generation: Access**)

**All other permissions can be set to "No Access"** - this is more secure and follows the principle of least privilege.

See `ELEVENLABS_API_KEY_SETUP.md` for detailed setup instructions.

## Note About ffmpeg Warning

You might see a warning about ffmpeg/avconv. This is only used for audio file processing. Since you're using ElevenLabs API (which returns MP3 files), you might not need ffmpeg, but it's recommended for better audio processing. You can ignore this warning if audio isn't critical for you.
