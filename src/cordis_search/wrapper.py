import pandas as pd

from .constants import *
from .search import *
from numpy import isnan

import logging
log = logging.getLogger(__name__)

def search(projects_dataframe, queries, **index_arguments):
    if isinstance(queries, str):
        queries = [queries]
    
    log.info(f"Creating index for dataframe of length {len(projects_dataframe)}.")
    whoosh_index = create_index(projects_dataframe, **index_arguments)

    for query in queries:
        log.info(f"Searching for query {query}.")
        ids = search_index(whoosh_index, query, **index_arguments)

        
        ids = [int(i) for i in ids]
        if len(ids) == 0:
            yield pd.DataFrame(columns=projects_dataframe.columns)
            
        projects_dataframe_with_id_index = projects_dataframe.set_index(ID_COL, drop=True)
        selected_projects = projects_dataframe_with_id_index.loc[ids]

        yield selected_projects

def summary(selected_projects, all_projects=None):
    print(f"Number of projects: {len(selected_projects)}")
    print("Total budget:","{:,.2f}".format(sum(selected_projects[TOTAL_COST_COL])), "EUR")
    if not isinstance(all_projects, type(None)):
        print(f"This equals to {sum(selected_projects[TOTAL_COST_COL])*100/sum(all_projects[TOTAL_COST_COL])} % of all projects")

    print("Total contribution EC:","{:,.2f}".format(sum(selected_projects[EC_MAX_CONTRIBUTION_COL])), "EUR")
    if not isinstance(all_projects, type(None)):
        print(f"This equals to {sum(selected_projects[EC_MAX_CONTRIBUTION_COL])*100/sum(all_projects[EC_MAX_CONTRIBUTION_COL])} % of all projects")

    print("EC contribution Per year:")
    selected_projects[YEAR_COL] = _get_year(selected_projects[START_DATE_COL])
    budget_per_year = selected_projects.groupby(YEAR_COL)[TOTAL_COST_COL].sum()
    
    ec_contribution_per_year = selected_projects.groupby(YEAR_COL)[EC_MAX_CONTRIBUTION_COL].sum()
    print(ec_contribution_per_year)
    return budget_per_year, ec_contribution_per_year

def _get_year(dates):
    return pd.DatetimeIndex(dates).year

