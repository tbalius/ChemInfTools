import sys, os
import tanimoto_tversky_cal_axon_lib as tccalc 
# writen by Trent Balius in 2018

def main():
  if (len(sys.argv) != 3): # if no input
     print "ERORR"
     print "syntax: python generate_chemaxon_hac.py smiles1 outputprefix"
     return

  smilesfile1   = sys.argv[1]
  outfileprefix = sys.argv[2]

  outfileF = outfileprefix +'.hac'

  pid = str(os.getpid()) # get the process idenifier so that we do not right over the same file. 

  # read in names from smiles file.  
  #names = []
  file1 = open(smilesfile1,'r')
  file2 = open(outfileF,'w')
  for line in file1:
      print line
      name = line.split()[1]  
      smiles = line.split()[0]  
      #print line, name
      #names.append(name)
      heavy = tccalc.heavyAtoms(smiles,pid)
      outfileF.write("%s %s\n"%(name,heavy))
  file1.close()
  file2.close()
  

main()

