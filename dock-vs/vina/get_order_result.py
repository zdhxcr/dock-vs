import sys

input_file = "order_result.txt"
if len(sys.argv) < 2:
    print("Usage: python script.py output_file")
    sys.exit(1)
output_file = sys.argv[1]  

results = []

with open(input_file, 'r') as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("out.") and line.endswith(".pdbqt"):
        filename = line
        if i + 1 < len(lines):
            score = lines[i + 1].strip()
            results.append((filename, score))
        i += 2
    else:
        i += 1

with open(output_file, 'w') as f:
    f.write("Filename,Score\n")
    for filename, score in results:
        f.write("%s,%s\n" % (filename, score))  
