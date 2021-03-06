import pandas as pd

from context import *
from cordis_search import search as sr

TEST_PROJECTS_FILE = pd.read_csv(RESOURCES_FOLDER+"fp7_test_projects.csv", sep=";")
print(TEST_PROJECTS_FILE)

def test_search():
    query = "multiculturalism"

    whoosh_index = sr.create_index(TEST_PROJECTS_FILE)
    ids = sr.search_index(whoosh_index, query)
    assert set(ids) == set(['267583', '287711'])

test_search()