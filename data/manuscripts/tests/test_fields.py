import data.manuscripts.fields as mflds


def test_get_flds():
    assert isinstance(mflds.get_flds(), dict)

def test_get_fld_names():
    fld_names = list(mflds.get_fld_names())  # Convert to list to ensure compatibility
    assert isinstance(fld_names, list)
    assert 'title' in fld_names  # Check if 'title' is in the field names

def test_get_disp_name():
    # Test with a valid field name
    disp_name = mflds.get_disp_name('title')
    assert disp_name == 'Title', f"Expected 'Title', but got {disp_name}"

def test_get_flds_keys():
    # Test if get_flds() returns a dictionary with expected keys
    flds = mflds.get_flds()
    assert isinstance(flds, dict), "get_flds() should return a dictionary."
    assert 'title' in flds.keys(), "Expected 'title' in the dictionary keys."
