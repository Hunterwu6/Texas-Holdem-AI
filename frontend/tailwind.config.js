/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'poker-bg': '#0F172A',
        'poker-table': '#065F46',
        'poker-felt': '#047857',
        'poker-primary': '#10B981',
        'poker-danger': '#EF4444',
        'poker-warning': '#F59E0B',
      },
    },
  },
  plugins: [],
}

