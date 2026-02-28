#!/bin/bash
# 批量复制 dock.in 并修改对应的 ligand 路径

for i in {1..10}; do
    cp dock.in dock-${i}.in
    sed -i "s|ligand-1/ligands-1.txt|ligand-${i}/ligands-${i}.txt|g" dock-${i}.in
    echo "✅ 已生成 dock-${i}.in"
done

