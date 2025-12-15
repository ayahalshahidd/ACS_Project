import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Determine backend protocol from environment variable
  // USE_HTTP=true means backend runs on HTTP, otherwise HTTPS
  const useHttp = process.env.USE_HTTP === 'true' || process.env.USE_HTTP === '1'
  const backendProtocol = useHttp ? 'http' : 'https'
  const backendUrl = process.env.VITE_API_URL || `${backendProtocol}://localhost:8000`
  
  // For HTTPS with misconfigured certificate, we need to accept it
  const secure = !useHttp ? false : undefined // false = accept self-signed/invalid certs
  
  console.log(`[Frontend] Proxy configured for: ${backendUrl}`)
  if (!useHttp) {
    console.log(`[Frontend] Accepting misconfigured certificate (secure: false)`)
  }
  
  return {
    plugins: [react()],
    server: {
      port: 3000,
      proxy: {
        '/api': {
          // VULNERABLE: Proxy configuration for data exposure demonstration
          // Automatically matches backend protocol (HTTP or HTTPS)
          target: backendUrl,
          changeOrigin: true,
          secure: secure,  // false = accept misconfigured certificate for HTTPS
        }
      }
    }
  }
})

