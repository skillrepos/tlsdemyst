#!/usr/bin/env bash
# Rebuilds the vendor/ folder from the official npm packages. You only need this to update
# the libraries; the files are already in vendor/.
# Needs Node.js. Run from the repo folder.
set -euo pipefail
WORK="$(mktemp -d)"; HERE="$(pwd)"
cd "$WORK" && npm init -y > /dev/null
npm install --ignore-scripts @huggingface/transformers@4.3.2 pdfjs-dist @orama/orama esbuild @modelcontextprotocol/sdk zod
mkdir -p "$HERE/vendor"
cp node_modules/pdfjs-dist/build/pdf.min.mjs node_modules/pdfjs-dist/build/pdf.worker.min.mjs "$HERE/vendor/"
cp node_modules/onnxruntime-web/dist/ort-wasm-simd-threaded.wasm node_modules/onnxruntime-web/dist/ort-wasm-simd-threaded.mjs "$HERE/vendor/"
echo "export * from '@orama/orama';" > orama-entry.js
npx esbuild orama-entry.js --bundle --format=esm --minify --outfile="$HERE/vendor/orama.min.js"
echo "export { pipeline, env } from '@huggingface/transformers';" > tf-entry.js
npx esbuild tf-entry.js --bundle --format=esm --platform=browser --minify \
    --alias:onnxruntime-web/webgpu=onnxruntime-web/wasm --outfile="$HERE/vendor/transformers.bundle.min.js"
cat > mcp-entry.js <<'EOF'
export { Client } from '@modelcontextprotocol/sdk/client/index.js';
export { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
export { InMemoryTransport } from '@modelcontextprotocol/sdk/inMemory.js';
export { z } from 'zod';
EOF
npx esbuild mcp-entry.js --bundle --format=esm --platform=browser --minify --outfile="$HERE/vendor/mcp-sdk.min.js"
# Token counter (Estimate the tokens): js-tiktoken with OpenAI's o200k_base table.
npm install --ignore-scripts js-tiktoken
cat > tok-entry.js <<'EOF2'
import { Tiktoken } from "js-tiktoken/lite";
import o200k_base from "js-tiktoken/ranks/o200k_base";
const enc = new Tiktoken(o200k_base);
export function pieces(text) {
  const ids = enc.encode(text); const out = []; let prev = "";
  for (let i = 0; i < ids.length; i++) { const cur = enc.decode(ids.slice(0, i + 1)); out.push({ id: ids[i], text: cur.slice(prev.length) }); prev = cur; }
  return out;
}
export function count(text) { return enc.encode(text).length; }
EOF2
npx esbuild tok-entry.js --bundle --format=esm --platform=browser --minify --outfile="$HERE/vendor/tokenizer.min.js"
ls -la "$HERE/vendor"
