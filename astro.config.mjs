import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://www.mingli-zhishu.com',
  integrations: [
    mdx(),
    tailwind({ applyBaseStyles: false }),
    sitemap(),
  ],
  trailingSlash: 'always',
  compressHTML: true,
  build: {
    inlineStylesheets: 'always',
  },
});
