# ElevenLabs API Key Setup - Exact Permissions Needed

## ✅ Required Permission for This Project

Based on the code analysis, this project **ONLY** uses the **Text-to-Speech** endpoint.

### You Only Need ONE Permission:

**📢 Text to Speech: Access**

- OR **Voice Generation: Access** (depending on which dialog you see)

### All Other Permissions: Set to "No Access"

You can safely set all other permissions to "No Access":

❌ **Not Needed:**

- Speech to Speech: No Access
- Speech to Text: No Access
- Sound Effects: No Access
- Audio Isolation: No Access
- Dubbing: No Access
- ElevenLabs Agents: No Access
- Projects: No Access
- Audio Native: No Access
- Voices: No Access (unless you want to customize voices)
- Forced Alignment: No Access
- Music Generation: No Access
- Administration: No Access
- History: No Access (unless you want to track usage)
- Models: No Access
- Pronunciation Dictionaries: No Access
- User: No Access

## Why Only Text-to-Speech?

Looking at the code in `server/tts_model.py`:

```python
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
```

The application **only** makes POST requests to:

- `https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}`

This is the **only** ElevenLabs endpoint used in the entire project.

## Step-by-Step Setup

1. **Go to ElevenLabs Dashboard**

   - Navigate to: https://elevenlabs.io/app/developers/api-keys
   - Click "+ Create Key"

2. **Set Permissions**

   - ✅ **Text to Speech: Access** (or **Voice Generation: Access**)
   - ❌ Everything else: **No Access**

3. **Create the Key**

   - Click "Create Key"
   - Copy the API key immediately (you won't be able to see it again!)

4. **Add to Your Project**

   - Create a `.env` file in the `server` directory:
     ```
     ELEVENLABS_API_KEY=your_api_key_here
     ```

5. **Restart Backend Server**
   ```bash
   cd server
   python app.py
   ```

## Security Best Practice

**Minimum Permissions Principle**: Only grant the permissions you actually need. This project only needs Text-to-Speech access, so:

- ✅ More secure (smaller attack surface)
- ✅ Better for API key management
- ✅ Prevents accidental usage of other features
- ✅ Easier to track what the key is used for

## What the API Key Does

The API key is used to:

1. Convert summary text to speech
2. Generate MP3 audio files
3. Serve audio to the frontend for playback

That's it! No other functionality requires the API key.

## Verification

After setting up the API key, test it:

1. Upload a PDF
2. Select "Summary" and "Audio" options
3. Click "Generate"
4. Check the Summary page - you should see an audio player
5. The audio should play the summary text

## Troubleshooting

### "Invalid API key" Error

- Verify the API key is correct
- Ensure "Text to Speech: Access" is enabled
- Check that the key is in the `.env` file

### "Rate limit exceeded" Error

- You've hit the free tier limit
- Wait a bit or upgrade your ElevenLabs plan
- The free tier has usage limits

### Audio Not Generating

- Check backend terminal for error messages
- Verify API key is set in `.env` file
- Ensure the key has "Text to Speech: Access" permission

## Summary

**Minimum Required Permissions:**

- ✅ **Text to Speech: Access** (or **Voice Generation: Access**)

**Everything Else:**

- ❌ **No Access**

That's all you need! Keep it simple and secure. 🎉
