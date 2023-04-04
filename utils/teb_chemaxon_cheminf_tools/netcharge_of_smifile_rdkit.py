import sys
from rdkit import Chem

## Writen by Trent Balius in the FNLCR, Dec, 2020

smifile = sys.argv[1]

fh = open(smifile)

for line in fh: 
   smi = line.split()[0]

   m2 = Chem.rdmolfiles.MolFromSmiles(smi)
   #netcharge2 = rdkit.Chem.rdmolops.GetFormalCharge(m)
   #netcharge = rdkit.Chem.rdmolops.GetFormalCharge(m2)
   netcharge = Chem.rdmolops.GetFormalCharge(m2)
   print('netcharge=%f\n'%netcharge)

