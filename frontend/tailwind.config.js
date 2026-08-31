/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "var(--color-primary)",
          hover: "var(--color-primary-hover)",
        },
        brand: {
          blue: "var(--color-brand-blue)",
        },
        sidebar: {
          border: "var(--color-sidebar-border)",
          darkBorder: "var(--color-sidebar-dark-border)",
        },
        tourism: {
          primary: "#003E83",   /* Deep Blue */
          secondary: "#2563eb", /* Royal Blue */
          accent: "#002e62",    /* Dark Primary */
          dark: "#18181b",      /* Dark Background */
          light: "#ffffff",     /* Light Background */
          border: "#f3f4f6",    /* Light Border */
          muted: "#6b7280"      /* Muted Text */
        }
      },
      fontFamily: {
        sans: ['Inter', 'Kantumruy Pro', 'sans-serif'],
        khmer: ['"Kantumruy Pro"', 'sans-serif'],
      },
      boxShadow: {
        'xs': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        '2xs': '0 0.5px 1px 0 rgba(0, 0, 0, 0.03), 0 0.5px 1.5px 0 rgba(0, 0, 0, 0.05)',
      },
      backdropBlur: {
        'xs': '2px',
      }
    },
  },
  plugins: [],
}
