import pytest
from common_code import load_templates
from rdkit import Chem


def generate_params():
    params = []
    for i, smiles, cxsmiles in load_templates():
        params.append(pytest.param(cxsmiles, id=f'line #{i}: {smiles}'))
    return params


@pytest.fixture(scope='module', params=generate_params())
def template(request):
    yield Chem.MolFromSmiles(request.param)


def test_valid_smiles(template):
    """
    Check that the template can be parsed
    """
    assert template


def test_single_conformer(template):
    """
    Check that the template has one single set of coordinates
    """
    assert template.GetNumConformers() == 1


def test_non_3d_coordinates(template):
    """
    Check that the template coordinates are flat
    """
    assert template.GetConformer().Is3D() is False


def test_single_fragment(template):
    """
    Check that the template contains a single molecule fragment
    """
    assert len(Chem.GetMolFrags(template)) == 1


def test_single_ring_system(template):
    """
    Check that the template contains a single ring system
    """
    ri = template.GetRingInfo()
    for bnd in template.GetBonds():
        if ri.NumBondRings(bnd.GetIdx()) == 0:
            raise ValueError('Invalid template, not a single ring system')
