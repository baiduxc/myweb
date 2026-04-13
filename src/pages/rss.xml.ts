import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { siteName, siteDesc, siteUrl } from '@data/site';

export async function GET() {
  const posts = await getCollection('blog');
  return rss({
    title: siteName,
    description: siteDesc,
    site: siteUrl,
    items: posts
      .filter((p) => !p.data.draft)
      .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf())
      .map((post) => ({
        title: post.data.title,
        description: post.data.description,
        pubDate: post.data.date,
        link: `/blog/${post.slug}/`,
      })),
    customData: `<language>zh-CN</language>`,
  });
}
