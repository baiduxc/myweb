/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'ink': '#1a1a1a',
        'ink-light': '#2d2d2d',
        'vermilion': '#c41e3a',
        'vermilion-light': '#d43b4f',
        'paper': '#faf7f0',
        'paper-dark': '#f0ebe0',
        'gold': '#c5a456',
        'gold-light': '#d4b870',
        'jade': '#4a7c59',
        'jade-light': '#5d9468',
        'water': '#2c5f6e',
        'water-light': '#3d7a8c',
        'earth': '#8b6914',
        'earth-light': '#a67c2e',
        'purple': '#6b4e8b',
        'purple-light': '#8a6ba8',
      },
      fontFamily: {
        'serif-cn': ['"Source Han Serif SC"', '"Noto Serif SC"', 'STSong', 'SimSun', 'serif'],
        'sans-cn': ['"PingFang SC"', '"Microsoft YaHei"', '"Source Han Sans SC"', '"Noto Sans SC"', 'sans-serif'],
      },
      backgroundImage: {
        'pattern': "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c5a456' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")",
        'cloud': "url(\"data:image/svg+xml,%3Csvg width='100' height='50' viewBox='0 0 100 50' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 25 Q30 10 40 25 Q50 10 60 25 Q70 10 80 25' stroke='%23c5a456' stroke-width='1' fill='none' opacity='0.3'/%3E%3C/svg%3E\")",
      },
      keyframes: {
        'spin-slow': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        'bounce-scroll': {
          '0%, 20%, 50%, 80%, 100%': { transform: 'translateY(0)' },
          '40%': { transform: 'translateY(-10px)' },
          '60%': { transform: 'translateY(-5px)' },
        },
      },
      animation: {
        'spin-slow': 'spin-slow 30s linear infinite',
        'bounce-scroll': 'bounce-scroll 2s infinite',
      },
    },
  },
  plugins: [],
};
