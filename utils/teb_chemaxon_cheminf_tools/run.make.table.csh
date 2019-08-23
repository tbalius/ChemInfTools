

#rm -rf images
#mkdir  images

set smiles_file = smo_my_ligands.smi 

foreach clusterfile (`ls cluster*.txt`)

#set cluster = 'cluster1'
set cluster = ${clusterfile:r:t}

#set ligandlist = `awk '{if(count > 1){print $1}; count=count+1}' $cluster.txt `
set ligandlist = `awk '{if(length($1) > 2){print $1};}' $cluster.txt `

   set filename = $cluster.html 
rm  $cluster.html

# header for table
cat << EOF > $cluster.html

<html> 
<head> 
<title>$cluster</title> 

   <hr width="100%"> 

   $cluster
 
   <table width="1600" border="0">

EOF

   echo "*******  $cluster ********"
   foreach lig ($ligandlist)
         set smiles1 = `grep $lig ${smiles_file} |  awk '{print $1}'`

         if !( -s images/$lig.png ) then
            #ls -l images/$lig.png
            echo "making image"
            molconvert png:w1000 -s "$smiles1" -2:e -o images/$lig.png
         endif

         echo "$lig $smiles1"

         echo "<tr>" >> $cluster.html
         echo "<td>  $lig </td>" >> $cluster.html
         echo "<td>  $smiles1 </td>" >> $cluster.html
         echo "<td>  <img src='images/$lig.png' width='100%' hight='100%'> </img> </td>" >> $cluster.html
         echo "</tr>" >> $cluster.html

   end # lig

cat << EOF >> $cluster.html

</table>
</html>

EOF

#exit

end #clusterfile
