import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    outDir: "../static/fightEvaluator/vue_dist",//change build output directory relative to project root
    assetsDir:"profit",
    rollupOptions:{
      output: {
        entryFileNames: 'profit.bundle.js',  // JS files in "js" folder
        chunkFileNames: `profit.js`,
        assetFileNames: 'profit.[ext]',
      },
    },
    emptyOutDir : true//will overwrite all content in directory

  }
})
