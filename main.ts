// Entry for the make.fun bounty "Sum up 21 November's world news in one image"
// (news-image-20261121).
//
// The entry is a small deterministic program: it copies the summary image
// bundled in this repository (assets/entry.png, a 1024x1024 PNG) to
// /output/entry.png. No network access, no randomness, no environment input,
// so every run writes exactly the same bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Verified 22 Nov 2026: two consecutive runs write byte-identical output,
// equal to assets/entry.png (sha256 2be0eef2…db884), 1024x1024, 121,948 bytes.
function main(): void {
  const root = dirname(fileURLToPath(import.meta.url));
  const bundled = join(root, "assets", "entry.png");
  mkdirSync("/output", { recursive: true });
  copyFileSync(bundled, "/output/entry.png");
}

main();
