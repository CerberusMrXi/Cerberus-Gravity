import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        cerberus: {
          bg: "#0a0e17",
          panel: "#111827",
          border: "#1e293b",
          muted: "#64748b",
          accent: "#3b82f6",
          danger: "#ef4444",
          warn: "#f59e0b",
          success: "#22c55e",
          gravity: "#8b5cf6",
          well: "#ec4899",
        },
      },
      fontFamily: {
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
