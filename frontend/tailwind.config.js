/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
      extend: {
          colors:{
              "black-primary": "#181A21",
              "red-secundary": "#f08080",
              "gray-text": "#676668",
          }
      },
      fontFamily: {
          FiraCode: ["FiraCode"]
      },
      conteiner: {
          padding: "2rem",
          center: true,
      },
      screens: {
          sm: "640px",
          md: "768px",
      },
  },
  plugins: [],
}

