import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1', // Use IPv4 to avoid IPv6 issues
    port: 5173,
    strictPort: true,
    hmr: {
      host: '127.0.0.1', // Use IPv4 for HMR WebSocket
      port: 5173, // Same port as server
      protocol: 'ws', // Explicit WebSocket protocol
    },
    watch: {
      usePolling: false,
    },
  },
})
