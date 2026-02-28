#!/bin/sh
#

path=/home/yxzhang/yxzhang/dock/dock-5/8tzx/p1p2-l/qvina/ligand
mkdir -p dock_info
mkdir -p result-pdbqt

for i in $path/*pdbqt;do
#echo $i
#j=$(basename  $i)
#j="similar-out."$i".pdbqt"
num=$(basename $i .pdbqt | cut -d'.' -f2)
pout=result-pdbqt/out."$num".pdbqt

cat > docking.conf <<EOF
receptor = protein_h.pdbqt
 ligand = $i
    out = $pout
 #AB
 center_x =-16.502
 center_y = 27.582
 center_z = 36.543

 size_x = 20
 size_y = 20
 size_z = 20


 cpu = 6

 # Default is 3
 energy_range = 3
 #energy_range = 6

 exhaustiveness = 25

 # Default is 9
 num_modes = 1

EOF
#run qvina
/home/yxzhang/Downloads/qvina/bin/qvina02 --config docking.conf  > ./dock_info/"$num".info 
done 
