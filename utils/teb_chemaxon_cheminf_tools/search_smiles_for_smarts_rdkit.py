
# This script was written by Trent Balius at FNLCR in 2019 

import sys
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs


def search_smiles_for_smarts(smiles_list,label_list,smarts,filename):
  fh = open(filename,'w')
  #for smiles in smiles_list:
  for i in range(len(smiles_list)):
     smiles = smiles_list[i]
     lab    = label_list[i]
     m = Chem.MolFromSmiles(smiles)
     patt = Chem.MolFromSmarts(smarts)
     if (m.HasSubstructMatch(patt)):
         print ("%s in %s"%(smarts, smiles))
         fh.write(smiles+' '+lab+'\n')
     m.GetSubstructMatch(patt)
  fh.close()

def main():

   #listsmiles = ['CCc1ccccc1', 'CCc1ccncc1', 'CCc1ncccc1']
   #smarts_patt = 'cnc'
   if (len(sys.argv) != 4): # if no input
        print (" (1) input file: list.smi")
        print (" (2) smart pattern")
        print (" (3) output file: list.smi")
        return

   in_smifile  = sys.argv[1]
   smarts_patt = sys.argv[2]
   out_smifile  = sys.argv[3]

   listsmiles = []
   listlabel = []
   fh = open(in_smifile)
   for line in fh:
       splitline = line.strip().split()
       smi = splitline[0]
       name = splitline[1]
       listsmiles.append(smi)
       listlabel.append(name)

   search_smiles_for_smarts(listsmiles,listlabel,smarts_patt,out_smifile)

main()
