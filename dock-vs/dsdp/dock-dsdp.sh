#!/bin/bash
#SBATCH -J DSDP-DBDC
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --gres=gpu:1
#SBATCH -p xhhgnormal
#SBATCH -o docking_%j.log

ulimit -s unlimited

# 初始化环境
source /work/home/acvwd4uw3y181/soft/DSDP/DSDP_redocking/env.sh
DSDP_PATH="/work/home/acvwd4uw3y181/soft/DSDP/DSDP_redocking"
source /work/home/acvwd4uw3y181/new/anaconda3/bin/activate
conda activate py312

# 设置路径
INPUT_DIR="ligand"
OUTPUT_DIR="ligand"
RESULT_FILE="dsdp_results.txt"
RECEPTOR="protein_h.pdbqt"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
# 参数设置
BOX_MIN="-11.416 -8.194 -18.505"
BOX_MAX="8.584 11.806 1.495"
EXHAUSTIVENESS=128
SEARCH_DEPTH=20
TOP_N=1

# 清空结果文件
> "$RESULT_FILE"

# 处理配体文件
for ligand in "$INPUT_DIR"/{mol.,lig.}*.pdbqt; do
    [ -e "$ligand" ] || continue  # 如果没有匹配的文件则跳过
      base_name=$(basename "$ligand")
    # 提取**部分（mol.或lig.后面的部分）
    out_name="out.${base_name#*.}"
    out_file="$OUTPUT_DIR/$out_name"

    echo "Processing: $base_name" | tee -a "$RESULT_FILE"

    "$DSDP_PATH"/DSDP \
        --ligand "$ligand" \
        --protein "$RECEPTOR" \
        --box_min $BOX_MIN \
        --box_max $BOX_MAX \
        --exhaustiveness $EXHAUSTIVENESS \
        --search_depth $SEARCH_DEPTH \
        --top_n $TOP_N \
        --out "$out_file" 2>&1 

done

echo "Docking completed!"
