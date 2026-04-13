/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'xuan': '#2B1B17',       // 玄色 - 深黑褐
        'zhu': '#8B2500',        // 朱砂红
        'zhu-light': '#A93226',  // 朱红浅
        'jin': '#B8860B',        // 金色
        'jin-light': '#DAA520',  // 浅金
        'xuan-paper': '#F5F0E8', // 宣纸色
        'xuan-paper-dark': '#EDE5D5',
        'mo': '#3D3D3D',         // 墨色
        'mo-light': '#5C5C5C',
        'qing': '#2E5A4B',       // 青色
        'qing-light': '#3D7A66',
        'tan': '#C4A47C',        // 檀色
        'rouge': '#C0392B',      // 胭脂
      },
      fontFamily: {
        'song': ['Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', 'serif'],
        'kai': ['Noto Serif SC', 'STKaiti', 'KaiTi', 'serif'],
        'hei': ['Noto Sans SC', 'Source Han Sans SC', 'Microsoft YaHei', 'sans-serif'],
      },
      backgroundImage: {
        'paper': "url(\"data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E\")",
      },
    },
  },
  plugins: [],
};
