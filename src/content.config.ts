// Checks on the site's content. content/site.json stays the one place the words live,
// because Artiscope Digital Home reads and writes it. These rules stop a build if something
// is malformed, so a mistake shows up before it reaches the live site:
// - every source has a title and, where it is online, a working-looking link;
// - every article and portfolio has its words and a web address.
// The links between entries (numbered sources, quiz rounds) are checked in src/lib/checks.mjs.
import { defineCollection } from "astro:content";
import { file } from "astro/loaders";
import { z } from "astro/zod";

const slug = z.string().regex(/^[a-z0-9][a-z0-9-]{0,80}$/, "a web address of small letters, digits and hyphens");

const sourcesCollection = defineCollection({
  loader: file("content/site.json", {
    parser: (text) => Object.entries(JSON.parse(text).sources || {}).map(([id, s]: [string, any]) => ({ ...s, id })),
  }),
  schema: z.object({
    title: z.string().min(1),
    pub: z.string().optional(),
    date: z.string().optional(),
    kind: z.string().optional(),
    // an offline record (such as gallery release records) has no link
    url: z.string().url().or(z.literal("")),
  }).passthrough(),
});

const articles = defineCollection({
  loader: file("content/site.json", { parser: (text) => (JSON.parse(text).articles || []).map((x: any) => ({ ...x, id: x.slug })) }),
  schema: z.object({
    slug,
    title: z.string().min(1),
    section: z.enum(["explained", "reviews", "features", "library"]),
    body: z.string().min(1),
    sources: z.array(z.string()).default([]),
  }).passthrough(),
});

const portfolios = defineCollection({
  loader: file("content/site.json", { parser: (text) => (JSON.parse(text).artists || []).map((x: any) => ({ ...x, id: x.slug })) }),
  schema: z.object({
    slug,
    name: z.string().min(1),
    published: z.boolean(),
  }).passthrough(),
});

export const collections = { sources: sourcesCollection, articles, portfolios };
