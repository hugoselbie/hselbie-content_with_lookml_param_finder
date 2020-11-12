import find_content_with_lookml_params as test_code


class mockRepoContent:
    # @staticmethod
    def get_repo():
        return test_code.path_file_parser('clients/sunrun/belvedere_test', '.lkml')


class mockRepo:
    @staticmethod
    def get_contents():
        return 'test'


class mockGithubConnection:
    @staticmethod
    def get_repo(*args, **kwargs):
        return mockRepo()


def test_repoContent():
    x = mockRepoContent().get_repo()
    assert isinstance(x, list) == True


def test_github_lkml_dict():
    x = mockGithubConnection().get_repo().get_contents()
    assert isinstance(x, str) is True
    # test = find_content_with_lookml_params.github_lkml('monkey100')
    # assert type(test[0]) == dict


# def test_lkml_objects():
#     test = find_content_with_lookml_params.github_lkml('monkey100')

#     assert html_objects.keys() == ['views']
