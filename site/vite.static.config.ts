import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  base: process.env.GITHUB_ACTIONS ? "/PowerBITraining/" : "/",
  plugins: [react()],
  build: {
    outDir: "static-dist",
    emptyOutDir: true,
  },
});
