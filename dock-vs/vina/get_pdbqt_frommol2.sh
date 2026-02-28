path=/home/yxzhang/yxzhang/dock/moleculars/fda/mol2-fda
#while read line ;do
for  i in *mol2;do
 label=$(echo $i | awk -F. '{print $1"."$2"."}')
 obabel -imol2 $i -opdb -O  ./pdb/"$label"pdb
 obabel  -ipdb   ./pdb/"$label"pdb  -opdbqt  -O   ./pdbqt/"$label"pdbqt
 #obabel -isdf $line -omol2 -O  ./mol2/"$label"mol2

done  
