
import sys,os
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
from rdkit.Chem import Descriptors 


## Writen by Trent Balius in the FNLCR, 2020
## mod by Trent Balius on Jan 25, 2023

def main():
  if not (len(sys.argv) == 2): # if no input
     print ("ERORR"                                                                    )
     print ("syntax: python logp.py smifile"            )
     return

  #pid = str(os.getpid()) # get the process idenifier so that we do not right over the same file. 
  #print (pid)

  smilesfile1 = sys.argv[1]


  fhi = open(smilesfile1,'r') 

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
     #netcharge = rdkit.Chem.rdmolops.GetFormalCharge(m2)

     logP = rdkit.Chem.Descriptors.MolLogP(m2)
     print('%s %s %f'%(smi,name,logP) )    

  fhi.close()


main()

