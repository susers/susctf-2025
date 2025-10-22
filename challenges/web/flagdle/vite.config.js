import { defineConfig } from "vite";
import { svelte, vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import { version } from "./package.json";
import obfuscatorPlugin from "vite-plugin-javascript-obfuscator";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/",
  plugins: [
    svelte({
      preprocess: vitePreprocess(),
    }),
    obfuscatorPlugin({
      options: {
        stringArrayIndexShift: false,
        stringArrayRotate: false,
        stringArrayShuffle: false,
      },
    }),
  ],
  build: {
    rollupOptions: {
      output: {
        assetFileNames: `[name]-v${version}.[ext]`,
        entryFileNames: `[name]-v${version}.js`,
        dir: "./dist",
      },
    },
  },
});
