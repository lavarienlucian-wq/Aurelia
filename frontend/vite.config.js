import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const isNetlify = process.env.NETLIFY === 'true'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: isNetlify ? '/' : '/static/frontend/',
  build: {
    outDir: isNetlify ? 'dist' : '../static/frontend',
    emptyOutDir: true,
  },
})
