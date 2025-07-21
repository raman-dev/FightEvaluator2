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
  //use for global scss variables and mixins
  // css: {
  //   preprocessorOptions: {
  //     scss: {
  //       additionalData: `
  //         @import "@/scss/_variables.scss";
  //         @import "@/scss/_mixins.scss";
  //       `
  //     }
  //   }
  // },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    outDir: "../fightEvaluator/static/fightEvaluator/vue-frontend",//change build output directory relative to project root
    assetsDir:"vue-frontend",
    rollupOptions:{
      output: {
        entryFileNames: 'frontend.bundle.js',  // JS files in "js" folder
        chunkFileNames: `frontend.js`,
        assetFileNames: 'frontend.[ext]',
      },
    },
    emptyOutDir : true//will overwrite all content in directory
  }
})
