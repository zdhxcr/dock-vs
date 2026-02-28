path=/home/zfzhao/zfzhao/new_vs/geminimol/gemin_file/dock/max/SDF
#while read line ;do
for  i in *sdf;do
 label=$(echo $i | awk -F. '{print $1"."$2"."}')
 obabel -isdf $i -opdb -O  ./pdb/"$label"pdb
 obabel  -ipdb   ./pdb/"$label"pdb  -opdbqt  -O   ./pdbqt/"$label"pdbqt
 #obabel -isdf $line -omol2 -O  ./mol2/"$label"mol2

done  
