
# This script was written by Trent Balius at FNLCR in 2019 

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
import sys

def read_fp(fpfile):
    fpvec = [] 
    fh1 = open(fpfile,'r')
    for line in fh1:
        fpvec.append(line.strip())
    return fpvec

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
      #fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4,1024)
      fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,2,1024) 
      # https://rdkit.readthedocs.io/en/latest/GettingStartedInPython.html
      # When comparing the ECFP/FCFP fingerprints and the Morgan fingerprints generated by the RDKit, remember that the 4 in ECFP4 corresponds to the diameter of the atom environments considered, while the Morgan fingerprints take a radius parameter. So the examples above, with radius=2, are roughly equivalent to ECFP4 and FCFP4.
      N = len(fp1bv)
      fh2.write("fingerprint = " )
      fpstr = ''
      for i in range(N):
            fh2.write('%d'%fp1bv[i]) 
            fpstr = fpstr + '%d'%fp1bv[i]
            if ((i+1)%8 == 0 and i!=N-1):
                 fh2.write('|') 
                 fpstr = fpstr + '|'
      fh2.write('\n') 
      fp_vec.append(fpstr)
  fh2.close()
  return fp_vec
