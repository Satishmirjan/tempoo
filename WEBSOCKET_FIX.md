# WebSocket Connection Error - Fixed

## Problem
The browser was trying to connect to `ws://localhost:5174/` but the Vite dev server was running on port 5173, causing WebSocket connection failures for Hot Module Replacement (HMR).

## Root Cause
1. Port mismatch between browser expectations and server port
2. IPv6 vs IPv4 binding issues (server was binding to `[::1]` IPv6 localhost)
3. HMR WebSocket configuration not explicitly set

## Solution Applied

### Updated `client/vite.config.js`:
- Set server host to `127.0.0.1` (IPv4) instead of `localhost` to avoid IPv6 issues
- Explicitly configured HMR WebSocket to use the same host and port
- Added `strictPort: true` to prevent port changes
- Set WebSocket protocol explicitly to `ws`

### Changes Made:
```javascript
server: {
  host: '127.0.0.1', // Use IPv4 to avoid IPv6 issues
  port: 5173,
  strictPort: true,
  hmr: {
    host: '127.0.0.1', // Use IPv4 for HMR WebSocket
    port: 5173, // Same port as server
    protocol: 'ws', // Explicit WebSocket protocol
  },
}
```

## How to Fix the Error

1. **Restart the dev server** (already done):
   ```bash
   cd client
   npm run dev
   ```

2. **Clear browser cache** or do a hard refresh:
   - Press `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac)
   - Or open DevTools → Network tab → Check "Disable cache"

3. **Close and reopen the browser tab** if the error persists

4. **Verify the server is running on the correct port**:
   - Check terminal output - should show: `Local: http://127.0.0.1:5173/`
   - The WebSocket should now connect to `ws://127.0.0.1:5173/`

## Verification

After restarting:
1. Open browser DevTools (F12)
2. Go to Console tab
3. Check for WebSocket connection errors
4. Should see: `[vite] connecting...` followed by `[vite] connected.`

## Additional Notes

- The error was harmless - it only affects HMR (Hot Module Replacement)
- The application still works without HMR, but you'll need to manually refresh the page to see changes
- With the fix, HMR should work automatically when you save files

## If Error Persists

1. **Check if port 5173 is available**:
   ```powershell
   netstat -ano | findstr "5173"
   ```

2. **Kill any processes using port 5173**:
   ```powershell
   # Find the process ID from netstat, then:
   taskkill /PID <process_id> /F
   ```

3. **Try a different port** in `vite.config.js`:
   ```javascript
   port: 3000, // or any other available port
   ```

4. **Check firewall settings** - ensure localhost connections are allowed

