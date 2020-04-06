
# This script was written by Trent Balius at FNLCR in 2019 

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
import sys

## this function reads in smiles and writes out the footprints.
## it returns a footprint vector
def get_fp(infile,outfile):
  fpvec = []
  fh1 = open(infile,'r')
  lines = fh1.readlines()
  fh1.close()
  fh2 = open(outfile,'w')
  smiles_list = []
  for line in lines:
     splitline = line.split()
     if len(splitline) > 2:
        print (line)
        print ("ERROR:len(smiles) > 2")
        exit()
     print (splitline)

     smiles_list.append(splitline[0])
     #print "simles = " + str(smiles);
  fp_vec = []
  for smiles in smiles_list:
      m1 = Chem.MolFromSmiles(smiles)
      #fp1 = AllChem.GetMorganFingerprint(m1,4)
      #fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4)
      #fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4,2048)
      fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4,1024)
      N = len(fp1bv)
      fh.write("fingerprint = " )
      fpstr = ''
      for i in range(N):
            fh2.write('%d'%fp1bv[i]) 
            fpstr = fpstr + fp1bv[i]
            if ((i+1)%8 == 0 and i!=N-1):
                 fh2.write('|') 
                 fpstr = fpstr + '|'
      fh2.write('\n') 
      fp_vec.append(fpstr)
  fh2.close()
  return fp_vec
