import data.manuscripts.fields as mflds


def test_get_flds():
    assert isinstance(mflds.get_flds(), dict)

def test_get_fld_names():
    fld_names = list(mflds.get_fld_names())  # Convert to list to ensure compatibility
    assert isinstance(fld_names, list)
    assert 'title' in fld_names  # Check if 'title' is in the field names

