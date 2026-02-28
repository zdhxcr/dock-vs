#!/bin/bash

in_f="$1"
mol_num=1
keyword="@<TRIPOS>MOLECULE"

tmp_f="tmp.mol2"

echo -n "" > "$tmp_f"

while IFS= read -r line; do
	if [[ "$line" == $keyword ]];then
	   if [ -s "$tmp_f" ]; then
		mv "$tmp_f" "fda.${mol_num}.mol2"
		((mol_num++))
	   fi 
	fi
	echo "$line" >> "$tmp_f"
done < "$in_f"

if [ -s "$tmp_f" ];then
	mv "$tmp_f" "fda.${mol_num}.mol2"
fi

echo "done"
