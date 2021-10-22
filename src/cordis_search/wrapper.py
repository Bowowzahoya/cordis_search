from .constants import *
from .search import *

def search(projects_dataframe, query, **index_arguments):
    whoosh_index = create_index(projects_dataframe, **index_arguments)
    ids = search_index(whoosh_index, query, **index_arguments)

    projects_dataframe = projects_dataframe.set_index(ID_COL, drop=True)
    print(projects_dataframe)
    ids = [int(i) for i in ids]
    selected_projects = projects_dataframe.loc[ids]

    return selected_projects