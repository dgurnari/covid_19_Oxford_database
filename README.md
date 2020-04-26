# covid_19_Oxford_database

 downloads the entire dataset at http://databank.worldbank.org/data/download/WDI_csv.zip

 converts it to a pandas dataframe and select only the rowns witch indicators are in interesting_indicators.cvs

 this seems to be the easiest way to go, but there are also API and a python wrapper
 https://wbdata.readthedocs.io/en/stable/index.html
 but it is not very flexible
