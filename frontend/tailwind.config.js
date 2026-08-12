/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        tourism: {
          primary: "#0F766E",   /* Deep Teal */
          secondary: "#14B8A6", /* Bright Teal */
          accent: "#0D9488",    /* Medium Teal */
          dark: "#0F172A",      /* Slate 900 */
          light: "#F8FAFC",     /* Slate 50 */
          border: "#E2E8F0",    /* Slate 200 */
          muted: "#64748B"      /* Slate 500 */
        }
      },
      fontFamily: {
        sans: ['Inter', 'Kantumruy Pro', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
