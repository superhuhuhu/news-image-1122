// news-image-20261122: deliver the front page for 22 November 2026.
//
// The picture is rendered on the build machine by build/render.py and
// committed here as entry.png. This program only moves that exact file
// into the output directory, so repeated runs are byte-identical. It
// never touches the network and never uses randomness: the sandbox
// only needs the file, a copy, and two sanity checks (PNG signature
// and the 1 MiB size cap).

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const SIZE_LIMIT = 1048576;

const here = dirname(fileURLToPath(import.meta.url));
const bundled = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const destination = join(outputDir, "entry.png");

if (!existsSync(bundled)) {
  console.error(`bundled image missing: ${bundled}`);
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(bundled, destination);

const firstBytes = readFileSync(destination).subarray(0, PNG_SIGNATURE.length);
if (!firstBytes.equals(PNG_SIGNATURE)) {
  console.error("output failed the PNG signature check");
  process.exit(1);
}

// The IHDR chunk follows the 8-byte signature: 4-byte length, 4-byte
// type, then width and height as big-endian uint32s. The front page
// is drawn at exactly 1024 by 1024, so anything else is a bad build.
const header = readFileSync(destination).subarray(0, 32);
const width = header.readUInt32BE(16);
const height = header.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  console.error(`unexpected image size: ${width}x${height}`);
  process.exit(1);
}

const bytes = statSync(destination).size;
if (bytes > SIZE_LIMIT) {
  console.error(`output is ${bytes} bytes, above the 1 MiB limit`);
  process.exit(1);
}

console.log(`wrote ${destination} (${bytes} bytes)`);
