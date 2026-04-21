export const siteName = '国学院';
export const siteDesc = '深入研习周易八卦、四柱八字、紫微斗数、奇门遁甲等传统易学知识，以现代视角解读千年智慧，助您明理知命、趋吉避凶。';
export const siteUrl = 'https://www.guoxueyuan.com';
export const siteAuthor = '国学院';
export const siteKeywords = '周易,八字,紫微斗数,风水,奇门遁甲,六爻,命理,国学,易学,天干地支,五行';

export const navLinks = [
  { href: '/', label: '首页' },
  { href: 'https://forum.example.com', label: '论坛', external: true },
  { href: 'https://paipan.example.com', label: '排盘', external: true },
  { href: 'https://jiemeng.example.com', label: '解梦', external: true },
  {
    href: '/bazi/',
    label: '基础知识',
    dropdown: true,
    children: [
      { href: '/bazi/', label: '八字命理', icon: '' },
      { href: '/wuxing/', label: '五行基础', icon: '☯' },
      { href: '/fengshui/', label: '风水堪舆', icon: '🧭' },
      { href: '/zhouyi/', label: '周易', icon: '☰' },
      { href: '/liuyao/', label: '六爻占卜', icon: '🪙' },
      { href: '/ziwei/', label: '紫微斗数', icon: '⭐' },
      { href: '/qimen/', label: '奇门遁甲', icon: '♜' },
    ],
  },
  { href: '/articles/', label: '全部文章' },
  { href: '/masters/', label: '专栏' },
  { href: '/books/', label: '书库' },
];

export const categories = [
  { slug: 'zhouyi', name: '周易', icon: 'mdi:book-education', color: 'from-ink to-ink-light', desc: '六十四卦精解', articles: 86, views: '12.3万' },
  { slug: 'bazi', name: '八字命理', icon: 'mdi:calendar-star', color: 'from-vermilion to-vermilion-light', desc: '四柱预测精要', articles: 124, views: '28.5万' },
  { slug: 'ziwei', name: '紫微斗数', icon: 'mdi:star-four-points', color: 'from-jade to-jade-light', desc: '十四主星详解', articles: 98, views: '19.8万' },
  { slug: 'fengshui', name: '风水堪舆', icon: 'mdi:compass', color: 'from-water to-water-light', desc: '形势理气双修', articles: 76, views: '15.2万' },
  { slug: 'qimen', name: '奇门遁甲', icon: 'mdi:chess-rook', color: 'from-earth to-earth-light', desc: '三奇六仪布局', articles: 54, views: '9.6万' },
  { slug: 'liuyao', name: '六爻占卜', icon: 'mdi:hand-peace', color: 'from-purple to-purple-light', desc: '纳甲筮法精解', articles: 62, views: '11.4万' },
];

export const masters = [
  {
    name: '明易先生',
    title: '周易研究专家',
    image: 'https://picsum.photos/seed/master1/400/300',
    bio: '深耕易学三十余载，专研周易卦象与人生哲学，著有《易道人生》等多部专著。',
    rating: '5.0',
    articleCount: 128,
    slug: 'mingyi',
  },
  {
    name: '玄微道长',
    title: '八字命理大师',
    image: 'https://picsum.photos/seed/master2/400/300',
    bio: '传承祖辈命理绝学，精通四柱八字、紫微斗数，擅长以现代视角解读传统命理。',
    rating: '4.9',
    articleCount: 96,
    slug: 'xuanwei',
  },
  {
    name: '清源居士',
    title: '奇门遁甲传人',
    image: 'https://picsum.photos/seed/master3/400/300',
    bio: '师承民间隐士，掌握奇门遁甲、六壬神课等古法，致力于传统文化现代化传播。',
    rating: '4.8',
    articleCount: 72,
    slug: 'qingyuan',
  },
];
