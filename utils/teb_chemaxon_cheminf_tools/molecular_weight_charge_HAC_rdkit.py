
import sys,os
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
from rdkit.Chem import Descriptors 


## Writen by Trent Balius in the FNLCR, 2020

def main():
  if not (len(sys.argv) == 3): # if no input
     print ("ERORR"                                                                    )
     print ("syntax: python tanimoto_cal_axon.py smiles1 outputprefix"            )
     return

  pid = str(os.getpid()) # get the process idenifier so that we do not right over the same file. 
  print (pid)

  smilesfile1 = sys.argv[1]
  outfileprefix = sys.argv[2]

  outfile1 = outfileprefix +'.txt'

  fhi = open(smilesfile1,'r') 
  fho = open(smilesfile1,'r') 

  flag_frist = False

  for line in fhi:
     if (flag_frist): 
         flag_frist = True 
         continue
     linesplit = line.split()
     smi = linesplit[0]
     name = linesplit[1]
     m2 = Chem.rdmolfiles.MolFromSmiles(smi)
     #netcharge2 = rdkit.Chem.rdmolops.GetFormalCharge(m)
     netcharge = rdkit.Chem.rdmolops.GetFormalCharge(m2)

     wt = rdkit.Chem.Descriptors.ExactMolWt(m2)
     hac = rdkit.Chem.Descriptors.HeavyAtomCount(m2)
     RB = rdkit.Chem.Descriptors.NumRotatableBonds(m2)
     print('%s %s %d %f %d %d'%(smi,name,netcharge,wt,hac,RB) )    

  fhi.close()


main()

