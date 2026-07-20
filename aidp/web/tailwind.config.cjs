// Tailwind configuration for the research hero UI
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brandOrange: '#e8702a',
        brandOrangeHover: '#d2611f',
      },
    },
  },
  plugins: [],
};
