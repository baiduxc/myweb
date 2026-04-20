import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    category: z.enum(['zhouyi', 'bazi', 'ziwei', 'fengshui', 'qimen', 'liuyao', 'wuxing', 'general']),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

// Book collection (for future PDF ebook parsing)
const booksCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    author: z.string(),
    dynasty: z.string().optional(),
    category: z.enum(['shan', 'yi', 'ming', 'xiang', 'bu']),
    description: z.string(),
    coverUrl: z.string().optional(),
    pdfUrl: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = {
  blog: blogCollection,
  books: booksCollection,
};
