#!/bin/bash

output="$1"

if [[ -z "$output" ]]; then
    echo "Usage: $0 output_file"
    exit 1
fi

echo "file score" > "$output"

find . -maxdepth 1 -name "*.dok" -type f -print0 |
while IFS= read -r -d '' file; do
    awk '
        NR==2 {
            for (i=1; i<=NF; i++) {
                if ($i=="Score:") {
                    print FILENAME, $(i+1)
                    exit
                }
            }
        }
    ' "$file"
done | sort -k2,2n >> "$output"

