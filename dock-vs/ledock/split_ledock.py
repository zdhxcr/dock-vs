#!/usr/bin/env python3
import os
import shutil
from math import ceil

# === 参数设置 ===
src_dir = "ligand"   # 原始小分子文件夹
n_groups = 10        # 要分成的小库数量
base_output = "/home/yxzhang/yxzhang/work-4-mg/md-4-ppdock/af3/6pai/big-lig-md/100ns/vs"  # 固定输出路径

# === 获取所有 mol2 文件 ===
ligands = sorted([f for f in os.listdir(src_dir) if f.endswith(".mol2")])
total = len(ligands)
print(f"总共有 {total} 个小分子，将分成 {n_groups} 个库。")

# === 每组的文件数 ===
per_group = ceil(total / n_groups)

for i in range(n_groups):
    start = i * per_group
    end = min((i + 1) * per_group, total)
    group_files = ligands[start:end]
    group_name = f"ligand-{i+1}"
    group_path = os.path.join(base_output, group_name)
    os.makedirs(group_path, exist_ok=True)

    # === 写列表文件 ===
    list_file = os.path.join(group_path, f"ligands-{i+1}.txt")
    with open(list_file, "w") as f:
        for fname in group_files:
            full_path = os.path.join(group_path, fname)
            f.write(full_path + "\n")
            # 将小分子复制到对应子文件夹
            shutil.copy2(os.path.join(src_dir, fname), os.path.join(group_path, fname))

    print(f"{group_name} 完成：{len(group_files)} 个文件。")

print("✅ 所有分割与列表生成完成！")

