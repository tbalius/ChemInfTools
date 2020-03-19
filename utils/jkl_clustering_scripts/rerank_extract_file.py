# 2016.11.01 Jiankun Lyu at Shoichet Lab

import sys

def read_extract_file(filename):

    file = open(filename)
    #lines = file.readlines()
    #file.close()

    #idlist = []
    #idDict_rank = {}
    #idDict_score = {}
    idDict_line = {}
    #count  = 0
    ## X is the Predicted value (sea_dock)
    ## Y is the accual value (sea)
    #firstline = True
    for line in file:
        #if firstline == True:
        #   firstline = False
        #   continue
        line = line.strip('\n')
        splitline = line.split()
        id = splitline[2]
        #score = splitline[21]
        #print score
        #idDict_rank[id] = count
        #idDict_score[id] = score
        idDict_line[id] = line
        #idlist.append(id)
        #count = count + 1

#    idlist.sort()
    file.close()
    #random.shuffle(idlist)

    #return idDict_score, idDict_line, idlist #idDict_rank, idDict_score, idDict_line, idlist
    #return idDict_score, idlist
    return idDict_line

if len(sys.argv) != 4:
	print "error:  this program takes 3 inputs."
	print "first input: extract_all.txt file"
	print "second input: ligands.name file"
	print "third input: output directory"
	exit()

extract_all_file  = sys.argv[1]
ligands_name_file = sys.argv[2]
outputdir         = sys.argv[3]

print "extract all file = " + extract_all_file

dict_line = read_extract_file(extract_all_file)

ligands_list = []
ligands_list_file = open(ligands_name_file,'r')

for line in ligands_list_file:
	#splitline = line.split()
	#ligands_list.append(splitline[0])
	splitline = line.split(',')
	ligands_list.append(splitline[2])
print "len(ligands.name) = "+str(len(ligands_list))

#output_decoys_file = open(outputdir+'/decoys.name','w')
output_extract_file = open(outputdir+'/extract_all.sort.uniq.re.txt','w')

for i in range(len(ligands_list)):
	output_extract_file.write(dict_line[ligands_list[i]]+'\n')
output_extract_file.close()

