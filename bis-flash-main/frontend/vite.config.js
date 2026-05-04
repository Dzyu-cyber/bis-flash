import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  oxc: {
    jsx: {
      runtime: 'automatic',
      importSource: 'react',
    },
  },
  optimizeDeps: {
    include: ['react', 'react-dom'],
    rolldownOptions: {
      moduleTypes: {
        '.js': 'jsx',
        '.jsx': 'jsx',
      },
    },
  },
})
