#!/bin/bash

tmpfile="tmp_scores.txt"
output="$1"

> "$tmpfile"  

for file in mol.*.dok; do
    if [[ -f "$file" ]]; then
        score=$(sed -n '2p' "$file" | grep -oP 'Score:\s+\K[-0-9.]+')
        echo "$score $file" >> "$tmpfile"
    fi
done
echo -e "file  score" > "$output"
sort -n "$tmpfile" | awk '{print $2, $1}' >> "$output"

rm "$tmpfile"


