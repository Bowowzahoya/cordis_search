# -*- coding: utf-8 -*-
"""
An example of a script to run queries on fp7 projects.
You can repeat the exact same script with just the file and instances of fp7
changed to h2020 to get results for H2020. Please note that the 
'fp7_projects_shortened.csv' file is shortened from the original version
to allow sharing on GitHub. Download your own file through the Cordis website.
"""
import pandas as pd
import cordis_search as cs

fp7_projects = pd.read_csv("fp7_projects_shortened.csv", sep=cs.SEPARATOR)
queries = pd.read_excel("Queries.xlsx", index_col = 0)["SciVal / Datenna Query"]

projects_generator = cs.search(fp7_projects, queries.values)
for area, selected_projects in zip(queries.index, 
                                   projects_generator):
    print(area)
    selected_projects.to_excel(f"out/fp7_{area}.xlsx")
    
    budget_per_year, ec_contribution_per_year = cs.summary(selected_projects)
    budget_per_year.to_excel(f"out/total_budget_fp7_{area}.xlsx")
    ec_contribution_per_year.to_excel(f"out/ec_budget_fp7_{area}.xlsx")
    
