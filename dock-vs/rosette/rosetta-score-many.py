import pyrosetta
from pyrosetta import *
import glob
import os

# ================= 配置区 =================
# 输出文件名
OUTPUT_FILE = "total_scores.txt"
# ==========================================

def score_single_pdb(pdb_file, scorefxn):
    """计算单个PDB文件的总能量"""
    try:
        print(f"Processing: {pdb_file} ...")
        pose = pose_from_pdb(pdb_file)
        total_score = scorefxn(pose)
        return total_score
    except Exception as e:
        print(f"Error processing {pdb_file}: {e}")
        return None

def batch_score_pdbs():
    """批量处理所有PDB文件"""
    
    # 1. 初始化PyRosetta
    print("Initializing PyRosetta...")
    pyrosetta.init("-ex1 -ex2 -mute all")  # -mute all 减少输出信息
    
    # 2. 创建打分函数
    scorefxn = create_score_function("ref2015")
    
    # 3. 获取所有PDB文件
    pdb_files = glob.glob("*.pdb")
    pdb_files.sort()  # 排序使结果更有规律
    
    if not pdb_files:
        print("No PDB files found in current directory!")
        return
    
    print(f"Found {len(pdb_files)} PDB files to process")
    
    # 4. 批量计算并保存结果
    with open(OUTPUT_FILE, 'w') as f:
        # 写入表头
        f.write(f"{'PDB File':<40} {'Total Score (REU)':>20}\n")
        f.write("-" * 60 + "\n")
        
        results = []
        
        for pdb_file in pdb_files:
            total_score = score_single_pdb(pdb_file, scorefxn)
            
            if total_score is not None:
                results.append((pdb_file, total_score))
                # 写入当前结果
                f.write(f"{pdb_file:<40} {total_score:>20.3f}\n")
                print(f"  Score: {total_score:.3f} REU")
            else:
                f.write(f"{pdb_file:<40} {'ERROR':>20}\n")
            
            print("")
        
        # 写入统计信息
        if results:
            scores = [score for _, score in results]
            avg_score = sum(scores) / len(scores)
            min_score = min(scores)
            max_score = max(scores)
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("Summary Statistics:\n")
            f.write(f"Total files processed: {len(results)}/{len(pdb_files)}\n")
            f.write(f"Average score: {avg_score:.3f} REU\n")
            f.write(f"Minimum score: {min_score:.3f} REU (best)\n")
            f.write(f"Maximum score: {max_score:.3f} REU (worst)\n")
            
            # 找出最佳和最差的结构
            best_file = min(results, key=lambda x: x[1])[0]
            worst_file = max(results, key=lambda x: x[1])[0]
            f.write(f"Best structure: {best_file}\n")
            f.write(f"Worst structure: {worst_file}\n")
    
    print(f"\nResults saved to: {OUTPUT_FILE}")
    print(f"Successfully processed {len(results)} out of {len(pdb_files)} PDB files")

def batch_score_with_details():
    """如果需要更详细的能量分项，使用这个函数"""
    
    print("Initializing PyRosetta...")
    pyrosetta.init("-ex1 -ex2")
    
    scorefxn = create_score_function("ref2015")
    pdb_files = glob.glob("*.pdb")
    pdb_files.sort()
    
    if not pdb_files:
        print("No PDB files found!")
        return
    
    # 创建详细结果文件
    detailed_output = "detailed_scores.txt"
    
    with open(detailed_output, 'w') as f:
        for pdb_file in pdb_files:
            print(f"\nProcessing: {pdb_file}")
            f.write(f"\n{'='*60}\n")
            f.write(f"File: {pdb_file}\n")
            f.write(f"{'='*60}\n")
            
            try:
                pose = pose_from_pdb(pdb_file)
                total_score = scorefxn(pose)
                
                # 写入总能量
                f.write(f"Total Score: {total_score:.3f} REU\n\n")
                
                # 获取并写入能量分项
                # 重定向show输出到字符串
                import io
                import sys
                
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                
                scorefxn.show(pose)
                
                energy_details = sys.stdout.getvalue()
                sys.stdout = old_stdout
                
                f.write(energy_details)
                
            except Exception as e:
                f.write(f"Error: {e}\n")
                print(f"Error processing {pdb_file}: {e}")
    
    print(f"\nDetailed results saved to: {detailed_output}")

if __name__ == "__main__":
    # 使用基本的批量打分功能
    batch_score_pdbs()
    
    # 如果需要详细的能量分项，取消下面的注释
    # batch_score_with_details()
