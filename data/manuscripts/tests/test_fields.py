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

def test_invalid_field_disp_name():
    # Test if get_disp_name() returns None for an invalid field name
    disp_name = mflds.get_disp_name('invalid_field')
    assert disp_name is None, "Expected None for an invalid field name, but got something else."

def test_missing_field_in_get_flds():
    # Check if a non-existent field is not in the FIELDS dictionary
    fields = mflds.get_flds()
    assert 'invalid_field' not in fields, "Non-existent field should not be present in the FIELDS dictionary."

