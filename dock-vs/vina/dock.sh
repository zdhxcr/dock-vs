#!/bin/sh
#

path=/DATA/yxzhang/dock/6pai/similar-dock
mkdir -p dock_info

for i in $path/*pdbqt;do
#echo $i
#j=$(basename  $i)
#j="similar-out."$i".pdbqt"
num=$(basename $i .pdbqt | cut -d'.' -f2)
pout=out."$num".pdbqt

cat > docking.conf <<EOF
# receptor = /home/yxzhang/yxzhang/dock/dacf15_rmb39.pdbqt
receptor = ../dcaf15-rbm39r2.pdbqt
 ligand = $i
 out    = $pout
 #AB
 center_x = 30.949
 center_y = 31.005
 center_z = 64.178

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

# Run vina
/home3/qwang/software/vina_1.2.3_linux_x86_64 --config docking.conf  > ./dock_info/"$num".info 
done 
