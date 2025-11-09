# FFmpeg Installation Guide (Optional)

## Why FFmpeg is Needed

The audio feature uses `pydub` to combine multiple audio chunks into a single file. `pydub` requires `ffmpeg` (or `avconv`) to process audio files.

**However**: The application now works **without ffmpeg**! It will use a simpler fallback method to combine audio chunks.

## Current Status

✅ **Audio works without ffmpeg** - The code now has a fallback method
⚠️ **Better quality with ffmpeg** - For best results, install ffmpeg

## Installing FFmpeg (Optional but Recommended)

### Option 1: Using Chocolatey (Easiest)

1. **Install Chocolatey** (if not already installed):
   - Open PowerShell as Administrator
   - Run:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```

2. **Install FFmpeg**:
   ```powershell
   choco install ffmpeg
   ```

3. **Restart your terminal** and verify:
   ```powershell
   ffmpeg -version
   ```

### Option 2: Manual Installation

1. **Download FFmpeg**:
   - Go to https://www.gyan.dev/ffmpeg/builds/
   - Download "ffmpeg-release-essentials.zip"

2. **Extract**:
   - Extract to `C:\ffmpeg`

3. **Add to PATH**:
   - Open "Environment Variables" (search in Windows)
   - Edit "Path" variable
   - Add: `C:\ffmpeg\bin`
   - Click OK

4. **Verify**:
   ```powershell
   ffmpeg -version
   ```

### Option 3: Using winget (Windows 10/11)

```powershell
winget install ffmpeg
```

## Verification

After installation, verify ffmpeg is available:

```powershell
ffmpeg -version
```

You should see version information.

## What Happens Without FFmpeg

The application will:
1. ✅ Still generate audio chunks from ElevenLabs
2. ✅ Combine chunks using a simpler method
3. ⚠️ Audio quality may be slightly lower
4. ✅ All functionality still works

## Benefits of Installing FFmpeg

- ✅ Better audio quality
- ✅ More reliable audio combination
- ✅ Support for more audio formats
- ✅ Better error handling

## Troubleshooting

### "ffmpeg not found" Error

1. **Check if ffmpeg is in PATH**:
   ```powershell
   where ffmpeg
   ```

2. **Restart terminal** after installation

3. **Restart backend server** after installing ffmpeg

### Audio Still Not Working

1. Check if audio chunks are being generated (look in `server/tts_chunks/`)
2. Check backend terminal for error messages
3. Verify API key is set correctly
4. Check network connectivity to ElevenLabs API

## Current Workaround

The application now works without ffmpeg by using a simpler audio combination method. However, for best results and reliability, installing ffmpeg is recommended.

## Summary

- ✅ **Audio works without ffmpeg** (uses fallback method)
- ⚠️ **Better with ffmpeg** (recommended for production)
- 🔧 **Easy to install** (choose one of the methods above)

