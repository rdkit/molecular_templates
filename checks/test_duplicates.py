import pytest
from common_code import load_templates
from rdkit import Chem
from rdkit.Chem import RegistrationHash


@pytest.mark.xfail(reason='we know we have some duplicates')
def test_check_duplicates():
    """
    Check if there are any duplicate templates.

    This test is slow, since it has to look at all the templates and
    generate hashes, so we want to run it only if we know all templates
    pass the basic requisites.
    """
    all_templates = {}
    duplicates = 0
    for i, smiles, cxsmiles in load_templates():
        mol = Chem.MolFromSmiles(cxsmiles)
        mol_layers = RegistrationHash.GetMolLayers(
            mol, enable_tautomer_hash_v2=True)
        mol_hash = RegistrationHash.GetMolHash(mol_layers)
        if (seen := all_templates.get(mol_hash, None)) is not None:
            seen_idx, seen_smiles = seen
            print(
                f'\nDuplicate template found:\n\t#{i} ({smiles}) is a duplicate of'
                f'\n\t#{seen_idx} ({seen_smiles})')
            duplicates += 1
        else:
            all_templates[mol_hash] = (i, smiles)
    assert duplicates == 0
