# cordis_search
 Search for H2020 and FP7 projects in the Cordis database

Download the data (Project publications) from:
 https://data.europa.eu/data/datasets/cordish2020projects?locale=en
 https://data.europa.eu/data/datasets/cordisfp7projects?locale=en
 
Two main functions are:

search(h2020_projects_dataframe, queries)
Which searches for projects given a number of queries (or one query). Notice that this function works as a generator.

h2020_projects_dataframe = pd.read_csv("h2020_projects.csv")
for selected_projects in search(h2020_projects_dataframe, queries):
	print(selected_projects)
	
--------------------------

summary(h2020_projects_dataframe) will print a summary on screen, and return the amounts per year (total and EC contribution) as two dataframes
