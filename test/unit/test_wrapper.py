import pandas as pd

from context import *
from cordis_search import wrapper as wr

TEST_PROJECTS_FILE = pd.read_csv(RESOURCES_FOLDER+"fp7_test_projects.csv", sep=";")
print(TEST_PROJECTS_FILE)

def test_search():
    query = "multiculturalism"

    selected_projects = wr.search(TEST_PROJECTS_FILE, query)
    assert set(selected_projects.index.to_list()) == set([267583, 287711])

def test_summary():
    wr.summary(TEST_PROJECTS_FILE)

test_summary()