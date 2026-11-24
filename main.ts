// post-x-promote-make-your-own-bounty-01: hand the post in.
//
// The entry is one post on X, made by the entrant (a quote of make.fun's
// make-your-own-bounty post, with a photo of its own attached). This program
// does the repository side of that handover: it copies POST.json, which names
// the post's address, from the repository into the output directory, so the
// house can read the post itself. It needs no network and no secrets.
//
// Run it locally the way the kit's guide says:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const REPO_ROOT = process.env.MAKEFUN_BOT_DIR ?? ".";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const postPath = join(REPO_ROOT, "POST.json");
if (!existsSync(postPath)) {
  console.error(`POST.json not found at ${postPath}`);
  process.exit(1);
}

const raw = readFileSync(postPath, "utf8");
let post: unknown;
try {
  post = JSON.parse(raw);
} catch {
  console.error("POST.json is not valid JSON");
  process.exit(1);
}
if (typeof post !== "object" || post === null || Array.isArray(post)) {
  console.error("POST.json must hold a JSON object");
  process.exit(1);
}
const url = (post as Record<string, unknown>).url;
if (typeof url !== "string" || url.length === 0) {
  console.error('POST.json must hold a "url" string');
  process.exit(1);
}
if (!/^(https?:\/\/)?(www\.|mobile\.)?(x\.com|twitter\.com)\/\w+\/status\/\d+/.test(url)) {
  console.warn(`warning: ${url} does not look like an X post address yet`);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(postPath, join(OUTPUT_DIR, "POST.json"));

// The photo is the post's own: the promo picture drawn for it, kept in the
// repository as photo.png. Hand it in beside POST.json, and prove both copies
// are byte for byte the files the repository holds.
const photoPath = join(REPO_ROOT, "photo.png");
if (!existsSync(photoPath)) {
  console.error(`photo.png not found at ${photoPath}`);
  process.exit(1);
}
copyFileSync(photoPath, join(OUTPUT_DIR, "photo.png"));
for (const name of ["POST.json", "photo.png"]) {
  const src = readFileSync(join(REPO_ROOT, name));
  const dst = readFileSync(join(OUTPUT_DIR, name));
  if (!src.equals(dst)) {
    console.error(`${name}: output copy differs from the repository file`);
    process.exit(1);
  }
  console.log(`${name}: ${src.length} bytes, copy verified`);
}
console.log(`wrote ${join(OUTPUT_DIR, "POST.json")} for ${url}`);
