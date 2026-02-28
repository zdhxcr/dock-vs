#!/usr/bin/env python3
import re

input_file = "result.txt"
output_file = "max_result.txt"

with open(input_file, 'r') as f:

    pattern = r"(out\..*?\.pdbqt)([\s\S]*?)(?=(?:out\..*?\.pdbqt|$))"
    matches = re.findall(pattern, f.read())

    list_result = []
    for match in matches:
        filename = match[0]
        values = [float(v) for v in match[1].strip().split('\n') if v.strip()]
        max_value = max(values, key=abs)  
        list_result.append([filename, max_value])


sorted_list = sorted(list_result, key=lambda x: abs(x[1]), reverse=True)

with open(output_file, 'w') as f:
    for filename, max_value in sorted_list:
        f.write(f"{filename} {max_value}\n")
