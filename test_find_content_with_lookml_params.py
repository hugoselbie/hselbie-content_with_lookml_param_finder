import find_content_with_lookml_params


def test_github_lkml_list():
    test = find_content_with_lookml_params.github_lkml('monkey100')
    assert type(test) == list


def test_github_lkml_dict():
    test = find_content_with_lookml_params.github_lkml('monkey100')
    assert type(test[0]) == dict


def test_lkml_objects():
    assert 