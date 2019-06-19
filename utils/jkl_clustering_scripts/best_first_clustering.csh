#2017.04.21 Jiankun Lyu at Shoichet Lab
#set the number of top ranking molecules you wanna cluster
set num_of_mol = $1
#set the tc threshold for the best first clustering of scaffold heads list
set tc = $2
#rename the original extract_all.sort.uniq.txt to extract_all.sort.uniq.all.txt
#mv extract_all.sort.uniq.txt extract_all.sort.uniq.all.txt
source ~tbalius/.cshrc_main
#extract specific lines from the extract_all.sort.uniq.all.txt file
head -${num_of_mol} extract_all.sort.uniq.txt > extract_all.top${num_of_mol}.sort.uniq.txt
#make a directory
mkdir best_first_clustering_${num_of_mol}_${tc}
cd best_first_clustering_${num_of_mol}_${tc}
#get SMILES
awk '{print $3}' ../extract_all.top${num_of_mol}.sort.uniq.txt > zincid.top${num_of_mol}.sort.uniq.txt
python ~jklyu/zzz.github/ChemInfTools/utils/teb_chemaxon_cheminf_tools/run.getstuff.from.postgreSQL.zinc_faster.py zincid.top${num_of_mol}.sort.uniq.txt extract_all.top${num_of_mol}.sort.uniq.smi
#add get smiles from ellman database
#create a file which contains two columns: the first column is zinc id and the second column is energy 
awk '{print $3" "$22}' ../extract_all.top${num_of_mol}.sort.uniq.txt > zincid.energy.top${num_of_mol}.sort.uniq.txt
#sort both the smi file and the zincid+energy file by zincid 
sort -k2 extract_all.top${num_of_mol}.sort.uniq.smi > extract_all.top${num_of_mol}.zincid.sort.uniq.smi
sort -k1 zincid.energy.top${num_of_mol}.sort.uniq.txt > zincid.sort.energy.top${num_of_mol}.sort.uniq.txt
#merge two files
paste -d" " extract_all.top${num_of_mol}.zincid.sort.uniq.smi zincid.sort.energy.top${num_of_mol}.sort.uniq.txt > temp
#sort the merged file by energy
sort -nk4 temp > temp.sort
#reformat the file for the Murcko scaffold analysis
awk '{print $1" "$2}' temp.sort > extract_all.top${num_of_mol}.sort.uniq.new.smi
#head -${num_of_mol} ../extract_all.sort.uniq.all.txt > ../extract_all.top${num_of_mol}.sort.uniq.txt
#add to check if the /scratch/username exist.
python ~jklyu/zzz.github/ChemInfTools/utils/teb_chemaxon_cheminf_tools/generate_chemaxon_fingerprints.py extract_all.top${num_of_mol}.sort.uniq.new.smi extract_all.top${num_of_mol}.sort.uniq

~jklyu/zzz.github/ChemInfTools/utils/best_first_clustering/best_first_clustering extract_all.top${num_of_mol}.sort.uniq.fp extract_all.top${num_of_mol}.sort.uniq.new.smi ${tc} ${num_of_mol}

#python /mnt/nfs/work/jklyu/AmpC/script/rerank_extract_file.py extract_all.top${num_of_mol}.sort.uniq.txt cluster_${num_of_mol}/best_first_clustering/${tc}/cluster_head.zincid .

#mv extract_all.sort.uniq.re.txt extract_all.sort.uniq.cluster.heads.txt 

#python /mnt/nfs/work/jklyu/AmpC/script/rerank_extract_file.py extract_all.top${num_of_mol}.sort.uniq.txt cluster_${num_of_mol}/top${num_of_mol}.scaffold.cluster.details.zincid .

#mv extract_all.sort.uniq.re.txt extract_all.sort.uniq.cluster.details.txt
