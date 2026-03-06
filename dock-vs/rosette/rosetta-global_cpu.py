import os
import multiprocessing
import time
import pyrosetta
from pyrosetta import pose_from_pdb, create_score_function
import pyrosetta.rosetta.protocols.flexpep_docking as flexpep_docking
import pyrosetta.rosetta.protocols.analysis as analysis
import pyrosetta.rosetta.core.scoring as scoring

# ================= ⚙️ 核心配置区 =================
INPUT_PDB = "6pai-clear.pdb"
OUTPUT_DIR = "global_result_pdb"
SC_FILENAME = "global_result.sc"
TOTAL_DECOYS = 50  # 全局对接建议加大采样
CPU_CORES = 10
# ============================================

def process_one_decoy(job_id):
    """子进程：独立初始化并执行一次全局搜索"""
    # 修正1：在函数内部初始化，并分配唯一种子 (参考 06_cpu.py)
    seed = int(time.time()) + job_id
    init_flags = f"-ex1 -ex2 -flexPepDocking:lowres_preoptimize true -run:jran {seed} -mute all"
    pyrosetta.init(init_flags)

    # 修正2：每个子进程独立加载结构，避免内存共享冲突
    work_pose = pose_from_pdb(INPUT_PDB)
    native_pose = work_pose.clone()
    
    # 协议设置
    fp_dock = flexpep_docking.FlexPepDockingProtocol()
    scorefxn = create_score_function("ref2015")
    iam = analysis.InterfaceAnalyzerMover(1)
    iam.set_pack_separated(True)
    
    # 执行对接
    fp_dock.apply(work_pose)
    
    # 计算指标
    total_score = scorefxn(work_pose)
    iam.apply(work_pose)
    i_sc = iam.get_interface_dG()
    rmsd = scoring.all_atom_rmsd(work_pose, native_pose)
    
    pdb_name = f"global_{job_id}.pdb"
    save_path = os.path.join(OUTPUT_DIR, pdb_name)
    work_pose.dump_pdb(save_path)
    
    return f"{pdb_name}\t{total_score:.3f}\t{i_sc:.3f}\t{rmsd:.3f}"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 初始化数据表
    with open(SC_FILENAME, "w") as f:
        f.write("description\ttotal_score\tI_sc\tAllAtom_RMSD\n")

    print(f">>> 全局对接启动！目标：{TOTAL_DECOYS} 个构象，核心：{CPU_CORES}")
    start_time = time.time()
    
    with multiprocessing.Pool(processes=CPU_CORES) as pool:
        # 使用 imap_unordered 实时获取结果
        results = pool.imap_unordered(process_one_decoy, range(1, TOTAL_DECOYS + 1))
        
        count = 0
        with open(SC_FILENAME, "a") as f:
            for line in results:
                count += 1
                f.write(line + "\n")
                if count % 10 == 0:
                    print(f"已完成: {count}/{TOTAL_DECOYS} | 进度: {count/TOTAL_DECOYS*100:.1f}%")

    print(f"\n全部完成！耗时: {time.time() - start_time:.1f} 秒")
