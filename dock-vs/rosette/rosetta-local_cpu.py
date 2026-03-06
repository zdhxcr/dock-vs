import pyrosetta
from pyrosetta import *
import os
import multiprocessing
import time

# 引用 PyRosetta 相关协议
import pyrosetta.rosetta.protocols.flexpep_docking as flexpep_docking
import pyrosetta.rosetta.protocols.analysis as analysis
import pyrosetta.rosetta.core.scoring as scoring

# ================= 实验参数设置 =================
INPUT_PDB = "6pai-clear.pdb"   
OUT_PREFIX = "refine_result"   
N_DECOYS = 50      # 测试跑50个，正式跑建议1000+
N_CORES = 6        # 设置你的核心数
OUTPUT_DIR = "local-docking_outputs"  # PDB 存放文件夹
# ==============================================

def worker_task(job_id):
    """单核计算任务：封装所有 Rosetta 操作"""
    # 1. 初始化每个进程，使用唯一随机种子
    # 使用时间+任务ID，彻底杜绝结果一致的问题
    seed = int(time.time()) + job_id
    init_flags = f"-ex1 -ex2 -flexPepDocking:pep_refine -run:jran {seed} -mute all"
    pyrosetta.init(init_flags)

    # 2. 读入结构
    pose = pose_from_pdb(INPUT_PDB)
    native_pose = pose.clone()

    # 3. 配置协议与打分
    fp_dock = flexpep_docking.FlexPepDockingProtocol()
    scorefxn = create_score_function("ref2015")
    iam = analysis.InterfaceAnalyzerMover(1)
    iam.set_pack_separated(True)

    # 4. 执行对接
    fp_dock.apply(pose)
    
    # 5. 计算各项指标
    total_score = scorefxn(pose)
    iam.apply(pose)
    i_sc = iam.get_interface_dG()
    rmsd = scoring.all_atom_rmsd(pose, native_pose)

    # 6. 保存 PDB 到子文件夹
    pdb_name = f"{OUT_PREFIX}_{job_id}.pdb"
    save_path = os.path.join(OUTPUT_DIR, pdb_name)
    pose.dump_pdb(save_path)

    # 返回一个字典，包含所有我们需要的数据
    return {
        "name": pdb_name,
        "total_score": round(total_score, 3),
        "I_sc": round(i_sc, 3),
        "RMSD": round(rmsd, 3)
    }

def run_main():
    # 自动创建结果文件夹
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f">>> 已创建输出目录: {OUTPUT_DIR}")

    print(f">>> 任务开始: 使用 {N_CORES} 核心生成 {N_DECOYS} 个构象...")
    
    # 启动进程池
    start_time = time.time()
    pool = multiprocessing.Pool(processes=N_CORES)
    
    # 将任务分发出去，收集所有返回的字典到 results 列表中
    results = pool.map(worker_task, range(1, N_DECOYS + 1))
    
    pool.close()
    pool.join()
    
    # --- 核心操作：使用 Python 原生语法进行排序 ---
    # 这里不需要 pandas，直接按字典里的 I_sc 键排序
    #results.sort(key=lambda x: x['I_sc'])

    # 写入 .sc 分数汇总文件
    sc_filename = f"{OUT_PREFIX}.sc"
    with open(sc_filename, "w") as f:
        # 写入表头
        f.write("description\ttotal_score\tI_sc\tRMSD\n")
        # 写入排序后的数据
        for res in results:
            line = f"{res['name']}\t{res['total_score']}\t{res['I_sc']}\t{res['RMSD']}\n"
            f.write(line)

    end_time = time.time()
 
    #best_res = min(results, key=lambda x:['I_sc']) the next row is a new try
    best_res = min(results, key=lambda x:x['I_sc'])

    print(f"\n" + "="*40)
    print(f"总耗时: {end_time - start_time:.2f} 秒")
    print(f"最优结果 (Top 1): {best_res['name']} (I_sc: {best_res['I_sc']})")
    print(f"所有 PDB 文件已存入: {OUTPUT_DIR}/")
    print(f"分数汇总表已生成: {sc_filename}")
    print("="*40)

if __name__ == "__main__":
    run_main()
