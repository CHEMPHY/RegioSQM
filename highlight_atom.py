import os
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole

name2smiles = {}

smiles_file_name = sys.argv[1]
pka_file_name = sys.argv[2]
svg_file_name = pka_file_name.split(".")[0]+".svg"

smiles_file = open(smiles_file_name, "r")
pka_file = open(pka_file_name, "r")

for line in smiles_file:
    words = line.split()
    name = words[0]
    smiles = words[1]
    name2smiles[name] = smiles

mols = []
names = []
atoms = []

for line in pka_file:
    words = line.split()
    name = words[0]
    smiles = name2smiles[name]
    atoms.append(map(int,words[1][:-1].split(",")))
    print
    m = Chem.MolFromSmiles(smiles)
    mols.append(m)
    Chem.Kekulize(m)
    names.append(name)
    Draw.DrawingOptions.includeAtomNumbers=True

img = Draw.MolsToGridImage(mols,molsPerRow=4,subImgSize=(200,200),legends=[x for x in names],useSVG=True,highlightAtomLists=atoms)


svg_file = open(svg_file_name, 'w')
svg_file.write(img.data)
svg_file.close()
os.system('sed -i "" "s/xmlns:svg/xmlns/" '+svg_file_name)
