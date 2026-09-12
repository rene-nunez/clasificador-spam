import {defineConfig} from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    tailwindcss()
  ],
  
  server: {
    proxy: {"/api": "http://localhost:8000"}, // redirige /api al backend (puerto 8000) en desarrollo
    port: 3000,
    host: true,
    strictPort: true
  }
})
