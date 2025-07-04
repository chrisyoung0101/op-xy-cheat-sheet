#!/usr/bin/env bash
set -euo pipefail

# max dimension in pixels
MAX=96

# output directory
OUT_DIR="assets/thumbs"
mkdir -p "$OUT_DIR"

# pick the right ImageMagick command
if command -v magick &>/dev/null; then
  IM_CLI="magick"
  IM_SUBCMD=""   # when using `magick`, you do: magick in.png -resize ... out.png
else
  IM_CLI="convert"
  IM_SUBCMD=""   # for convert we do the same: convert in.png -resize ... out.png
fi

for img in assets/*.{JPEG,JPEG,png,PNG}; do
  [[ -e "$img" ]] || continue

  out="$OUT_DIR/$(basename "$img")"
  # note the quotes around the resize argument so the shell doesn't treat '>' as a redirect
  $IM_CLI $IM_SUBCMD "$img" -resize "${MAX}x${MAX}>" "$out"
  echo "→ resized $(basename "$img") → $out"
done

echo "✅ All done! Resized images are in $OUT_DIR/"

