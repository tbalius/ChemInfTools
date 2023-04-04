
# This script was written by Trent Balius at FNLCR in 2019 

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
import sys

def make_fingerprint_file(smifilename,filename):
  fhr = open(smifilename)
  fhw1 = open(filename,'w')
  fhw2 = open(smifilename+'_mod','w')
  for line in fhr:
      splitline = line.strip().split() 
      smiles = splitline[0]
      name = splitline[1]
      #try:
      #  m1 = Chem.MolFromSmiles(smiles)
      #except: 
      #  print ("failed: name=%s;smi=%s"%(name,smiles))
      #  continue
      m1 = Chem.MolFromSmiles(smiles) 
      if m1 == None: 
         print ("failed: name=%s;smi=%s"%(name,smiles))
         continue 
      #fhw2.write("%s %s\n"%(smiles,name))
      fhw2.write("%s"%(line))
      #fp1 = AllChem.GetMorganFingerprint(m1,4)
      #fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4)
      #fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4,2048)
      fp1bv = AllChem.GetMorganFingerprintAsBitVect(m1,4,1024)
      N = len(fp1bv)
      fhw1.write("fingerprint = " )
      for i in range(N):
            fhw1.write('%d'%fp1bv[i]) 
            if ((i+1)%8 == 0 and i!=N-1):
                 fhw1.write('|') 
      fhw1.write('\n') 
  fhw1.close()
  fhw2.close()

def main():

   #listsmiles = ['CCc1ccccc1', 'CCc1ccncc1', 'CCc1ncccc1']
   if (len(sys.argv) != 3): # if no input
        print (" (1) input file: list.smi")
        print (" (2) output file: list.fp")
        return

   in_smifile = sys.argv[1]
   out_fpfile  = sys.argv[2]

   make_fingerprint_file(in_smifile,out_fpfile)

main()
