# .gitlab-ci/scripts/shell/generate-services.yml.sh

#!/bin/bash
mkdir -p .gitlab-ci
OUT=".gitlab-ci/services.yml"
echo "services:" > "$OUT"

find . -path "*/templates/vars.yml" | while read -r file; do
  CATEGORY=$(dirname "$(dirname "$file")")
  CATEGORY=${CATEGORY#./}

  NAME=$(yq eval '.service' "$file")
  DIR="$CATEGORY/$NAME"
  TRAEFIK=$(yq eval '.default_secured_with_traefik // true' "$file")
  VOLUMES=$(yq eval '.volume_dirs // []' "$file" | yq eval -o=json - | jq -c '.')

  echo "  - name: $NAME" >> "$OUT"
  echo "    category: $CATEGORY" >> "$OUT"
  echo "    service_dir: $DIR" >> "$OUT"
  echo "    vars_file: $file" >> "$OUT"
  echo "    default_secured_with_traefik: $TRAEFIK" >> "$OUT"
  echo "    volume_dirs: $VOLUMES" >> "$OUT"
done
