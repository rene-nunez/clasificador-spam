import {defineConfig} from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    tailwindcss()
  ],
  
  server: {
    proxy: {"/api": "http://localhost:8000"}, // redirige /api al backend (puerto 8000) en desarrollo
    port: 3000,
    host: true, // Acceso desde cualquier dispositivo en la red LAN (debug móvil)
    strictPort: true
    
    /*
      Nota: estas opciones solo configuran el servidor de desarrollo (npm run dev).
      No afectan al comportamiento del proyecto en producción (npm run build)
    */
  }
})