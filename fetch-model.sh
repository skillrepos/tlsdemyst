#!/usr/bin/env bash
# Optional: copy the text-to-numbers model into this site, so the lab page does not
# depend on huggingface.co being reachable from the conference network.
# Run once from the repo folder on a machine with normal internet access, then commit models/.
# Adds about 24 MB to the repo.
set -euo pipefail
BASE="https://huggingface.co/Xenova/all-MiniLM-L6-v2/resolve/main"
DEST="models/Xenova/all-MiniLM-L6-v2"
mkdir -p "$DEST/onnx"
for f in config.json tokenizer.json tokenizer_config.json; do
    curl -fL "$BASE/$f" -o "$DEST/$f"
done
curl -fL "$BASE/onnx/model_quantized.onnx" -o "$DEST/onnx/model_quantized.onnx"
ls -la "$DEST" "$DEST/onnx"
echo "Done. Commit the models/ folder. The lab page now loads the model from this site."
