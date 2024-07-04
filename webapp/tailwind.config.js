import defaultTheme from "tailwindcss/defaultTheme";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Open Sans", defaultTheme.fontFamily.sans],
      },
      colors: {
        primary: {
          50: "#f4f5f9",
          100: "#eceef3",
          200: "#dcdfe9",
          300: "#c6cbdb",
          400: "#aeb3cb",
          500: "#989cbc",
          600: "#8283a9",
          700: "#6f6f93",
          800: "#5b5b78",
          900: "#4d4e62",
          950: "#2d2d39",
        },
      },
    },
  },
  plugins: [],
};
