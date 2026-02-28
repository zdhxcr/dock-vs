#!/bin/sh
#

path=/DATA/yxzhang/dock/moleculars/fda/pdbqt
mkdir -p dock_info
mkdir -p result-pdbqt

for i in $path/*pdbqt;do
#echo $i
#j=$(basename  $i)
#j="similar-out."$i".pdbqt"
num=$(basename $i .pdbqt | cut -d'.' -f2)
pout=result-pdbqt/out."$num".pdbqt

cat > docking.conf <<EOF
# receptor = /home/yxzhang/yxzhang/dock/dacf15_rmb39.pdbqt
receptor = 
 ligand = $i
    out = $pout
 #AB
 center_x =
 center_y = 
 center_z = 

 size_x = 20
 size_y = 20
 size_z = 20


 cpu = 6

 # Default is 3
 energy_range = 3
 #energy_range = 6

 exhaustiveness = 25

 # Default is 9
 num_modes = 9

EOF

# Run vina
/home3/qwang/software/vina_1.2.3_linux_x86_64 --config docking.conf  > ./dock_info/"$num".info 
done 
