#!/bin/bash

# 创建result文件夹（如果不存在）
mkdir -p result

# 循环遍历所有ligand-*/文件夹
for dir in ligand-*/; do
    # 检查目录是否存在
    if [ -d "$dir" ]; then
        # 复制该目录下的所有*dok文件到result文件夹
        cp "$dir"*dok result/ 2>/dev/null
    fi
done

echo "复制完成！所有ligand-*/文件夹中的dok文件已复制到result文件夹"
