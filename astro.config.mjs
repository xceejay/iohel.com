// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import { remarkReadingTime } from "./src/lib/remark.mjs";

// https://astro.build/config
export default defineConfig({
  site: "https://iohel.com",
  markdown: {
    remarkPlugins: [remarkReadingTime],
    shikiConfig: {
      theme: "gruvbox-dark-medium",
    },
  },
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [
    sitemap(),
    mdx({
      optimize: true,
      syntaxHighlight: "shiki",
    }),
  ],
  experimental: {
    fonts: [
      {
        name: "Grenze",
        cssVariable: "--font-grenze",
        provider: "local",
        variants: [
          {
            src: ["./src/assets/fonts/Grenze/grenze-v16-latin-300.woff2"],
            style: "normal",
            weight: 300,
          },
          {
            src: ["./src/assets/fonts/Grenze/grenze-v16-latin-regular.woff2"],
            style: "normal",
            weight: 400,
          },
          {
            src: ["./src/assets/fonts/Grenze/grenze-v16-latin-500.woff2"],
            style: "normal",
            weight: 500,
          },
          {
            src: ["./src/assets/fonts/Grenze/grenze-v16-latin-600.woff2"],
            style: "normal",
            weight: 600,
          },
          {
            src: ["./src/assets/fonts/Grenze/grenze-v16-latin-700.woff2"],
            style: "normal",
            weight: 700,
          },
        ],
      }
      ,
      {
        name: "InterVariable",
        cssVariable: "--font-inter-variable",
        provider: "local",
        variants: [
          {
            src: ["./src/assets/fonts/Inter/InterVariable.woff2"],
            style: "normal",
            weight: "variable",
          },
        ],
      },
    ],
  },
});
