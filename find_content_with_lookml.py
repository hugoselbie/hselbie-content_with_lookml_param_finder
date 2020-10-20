import looker_sdk
import pandas as pd
import glob
import lkml
import json
import configparser as ConfigParser
from github import Github
import base64

ini_file = 'looker.ini'
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read(ini_file)

github_token = config.get('Github', 'github_token')
sdk = looker_sdk.init40(config_file=ini_file)

g = Github(github_token)


def github_lkml(repo_name: str):
    """connect to repo with lookml, iterate through lookml and returns list
    of parsed lookml

    Args:
        repo_name (str): name of repo (not path)

    Returns:
        [list]: list of lookml elements in repo 
    """
    g = Github(github_token)
    authed_user = g.get_user()
    repo = authed_user.get_repo(repo_name)
    contents = repo.get_contents("", ref='master')
    lookml = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            x = base64.b64decode(file_content.content).decode('ascii')
            lookml.append(lkml.load(x))
            
    return lookml


def path_file_parser(path: str, extension: str, recursive=True):
    """Return a list of Full File Paths
    Parameters:
    path (str): Parent Directory to parse
    extension (Optional) (str): fil e extension to search, i.e. ".txt"
    recursive (Boolan): Defaults to false to check child directories
    """
    return [f for f in glob.glob(path + "**/*" + extension, recursive=recursive)]


def file_parse_lkml(file_paths: list):
    """Iterate through local file paths
    and return a list of lookml files with an element 
    for each lookml file]

    Args:
        file_paths (list): [a list of local path strings]

    Returns:
        [list]: [list of parsed lookml]
    """
    response_list = []
    for path in file_paths:
        with open(path, 'r') as file:
            print(lkml.load(file))
            # pass
    # return response_list


def find_html_lkml_objects(lookml_list: list):
    """[summary]

    Args:
        lookml_list (list): [description]

    Returns:
        [type]: [description]
    """
    html_elements = {}
    test = lookml_list
    for lookml_object in lookml_list:
        parsed = lkml.load(lookml_object)
        view_name = parsed['views'][0]['name']
        elements = ['dimension_groups', 'dimensions', 'measures']
        fields = []
        for lkml_element in parsed['views'][0].keys():
            if lkml_element in elements:
                
                for obj in parsed['views'][0][lkml_element]:
                    if 'html' in obj.keys():
                        fields.append(view_name+'.'+obj['name'])
        html_elements[view_name] = fields
    return html_elements


#TODO create a create query representation of this look for more extensibility     
def compare_html_objects():
    """[summary]

    Returns:
        [type]: [description]
    """
    dash = sdk.run_look(675, 'json')
    dash = json.loads(dash)
    df = pd.DataFrame(dash)
    df = df[(df['unused_dashboards'] == 0)]
    return df


if __name__ == "__main__":
    
    # test = find_html_lkml_objects(lookml_list=lookml_list)
    # print(test)
    path = 'clients/sunrun/belvedere_test'
    lookml_files = path_file_parser(path=path, extension='view.lkml')
    print(file_parse_lkml(file_paths=lookml_files))
    # x = list_lookml(file_paths=lookml_files)
    # print(x)
    y = github_token('monkey100')
    # print(y)
    # list_lookml(y) 
    
    # l
    # html_fields = find_html_lkml_objects(file_paths=lookml_files)
    # test = []
    # df = compare_html_objects()
    # for row in df.itertuples():
        # fields = row[4]
        # try:
        #     fields = json.loads(fields)
        #     for field in fields:
        #         for view, dimensions in html_fields.items():
        #             for dim in dimensions:
        #                 if dim == field:
        #                     test.append(f'dashboard title = {row[1]}, dashboard id = {row[2]}, element title = {row[3]}')
        #                 else:
        #                     pass
                
        # except TypeError:
        #     pass
    # print(test)
    