
# This script was written by Trent Balius at FNLCR in 2019 

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
import sys

def make_fingerprint_file(smiles_list,filename):
  fh = open(filename,'w')
  for smiles in smiles_list:
      m1 = Chem.MolFromSmiles(smiles)
      #fp1 = AllChem.GetMorganFingerprint(m1,4)
      #fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4)
      #fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4,2048)
      fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4,1024)
      N = len(fp1bv)
      fh.write("fingerprint = " )
      for i in range(N):
            fh.write('%d'%fp1bv[i]) 
            if ((i+1)%8 == 0 and i!=N-1):
                 fh.write('|') 
      fh.write('\n') 
  fh.close()

def main():

   #listsmiles = ['CCc1ccccc1', 'CCc1ccncc1', 'CCc1ncccc1']
   if (len(sys.argv) != 3): # if no input
        print (" (1) input file: list.smi")
        print (" (2) output file: list.fp")
        return

   in_smifile = sys.argv[1]
   out_fpfile  = sys.argv[2]

   listsmiles = []
   fh = open(in_smifile)
   for line in fh:
       splitline = line.strip().split() 
       smi = splitline[0]

       listsmiles.append(smi)
   make_fingerprint_file(listsmiles,out_fpfile)

main()
