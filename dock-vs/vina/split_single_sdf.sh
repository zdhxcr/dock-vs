#!/bin/bash

#input_name
input_file="extra_JK.sdf"
# out_name
output_prefix="extra_JK"

# start_number
count=1

output_file="${output_prefix}.${count}.sdf"

while IFS= read -r line
do
    
    if [[ "$line" == "\$\$\$\$" ]]; then
        echo "$line" >> "$output_file"
        count=$((count + 1))
        output_file="${output_prefix}.${count}.sdf"
    else
        echo "$line" >> "$output_file"
    fi
done < "$input_file"

echo "done, all file number ${count} "
