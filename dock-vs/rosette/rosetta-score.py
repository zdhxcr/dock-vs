import pyrosetta
from pyrosetta import *

# ================= 配置区 =================
# 必须使用和另一个程序一模一样的 PDB 文件！
INPUT_PDB = " 6pai-clear.pdb"   
# ==========================================

def just_score_it():
    # 1. 初始化
    # 保持和之前一样的参数，确保环境一致
    pyrosetta.init("-ex1 -ex2")

    # 2. 加载结构
    print(f"reading: {INPUT_PDB} ...")
    pose = pose_from_pdb(INPUT_PDB)

    # 3. 创建打分函数 (Ref2015)
    scorefxn = create_score_function("ref2015")

    # 4. === 核心步骤：直接打分 ===
    # 注意：这里没有任何 apply, minimize, dock 操作
    # 仅仅是把尺子放上去量一下
    total_score = scorefxn(pose)

    print("\n" + "="*40)
    print(f"【compare】 Total Score: {total_score:.3f} REU")
    print("="*40 + "\n")

    # 5. === 进阶步骤：查看能量分项 ===
    # 这会打印出每一项的具体得分 (比如 fa_atr, fa_rep, fa_elec)
    # 如果两个程序总分不同，对比这个表就能知道是谁在捣鬼
    print("details...")
    scorefxn.show(pose)

if __name__ == "__main__":
    just_score_it()
