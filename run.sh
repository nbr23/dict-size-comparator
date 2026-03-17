#!/bin/sh
set -e

if [ $# -eq 0 ]; then
  echo "Usage: $0 <locale_codes>" >&2
  echo "  e.g. $0 en_GB,fr,pt_BR" >&2
  exit 1
fi

LOCALES="$1"

HUNSPELL_PACKAGES=""
IFS=','
for locale in $LOCALES; do
  pkg="hunspell-$(echo "$locale" | tr '[:upper:]_' '[:lower:]-')"
  HUNSPELL_PACKAGES="$HUNSPELL_PACKAGES $pkg"
done
unset IFS

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$SCRIPT_DIR/output"

echo "BUILDING: docker build --build-arg HUNSPELL_PACKAGES=\"$HUNSPELL_PACKAGES\" -t languages \"$SCRIPT_DIR\""
docker build --build-arg HUNSPELL_PACKAGES="$HUNSPELL_PACKAGES" -t languages "$SCRIPT_DIR" > /dev/null
docker run --rm \
  -v "$SCRIPT_DIR/count_letters.py:/count_letters.py:ro" \
  -v "$SCRIPT_DIR/output:/output" \
  languages \
  python3 /count_letters.py "$LOCALES"
