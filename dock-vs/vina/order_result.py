#!/usr/bin/env python3
import re

input   =   "result.txt"
output  =   "order_result.txt"

with open(input, 'r') as f:
    parttern = r"(out\..*?\.pdbqt)([\s\S]*?)(?=(?:out\..*?\.pdbqt|$))"
    matches = re.findall(parttern, f.read())
    
    list_result = [[match[0], match[1].strip()] for match in matches]

#    print(list_result)

sorted_list = sorted(list_result, key=lambda x: float(x[1].split('\n')[0]))

#for lines in sorted_list:
#    print(lines)

with open(output, 'w') as f:
    for lines in sorted_list:
        f.write(lines[0]+'\n')
        f.write(lines[1]+'\n')
