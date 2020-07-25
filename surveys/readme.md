# covid_19_Oxford_database
# SURVEYS TABLE

# Integrated Value Survey

## About the Integrated Values Survey and data fetching
The Integrayed Value Survey dataset is obtained by merging together six waves of the World Value Survey with four waves of the European Value Survey.\
https://europeanvaluesstudy.eu/methodology-data-documentation/previous-surveys-1981-2008/integrated-values-surveys-1981-2014/

Since this integrated dataset is not directly available we personally merged it folowing the official guidelines. Our version can be found at
https://drive.google.com/drive/folders/1ug6_ndeEi4OhmAZJeXiZmG7BO6T5bPX9?usp=sharing
and contains 1430 variables and 513529 observations. In the same folder we include the log of the merging procedure.

## Variables Processing and Aggregation
We considered only a subset of all the questions found in the surveys, this list can be found in the file IVS_Variable_List.cvs

We aim to provide two different levels of aggregation:
- by Survey, Wave and Country;
- by Survey, Wave, Country and local region.

Before being aggregate each individual answer is one-hot encoded. \
For each answer in the dataset, a weight is available to compensate for small deviations in the sample at the country level.\
http://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=WEIGHT \
When aggregating at the country level we choosed to rescale each answer, when aggregating at the region level we choosed not to since regional weight are not present. \
We used the aritmetic mean as the aggregating function, since each answer was one hot encoded we can interpret the resulting values as frequencies.

## PROPERTIES DICTIONARY
As an effect of the one hot encoding the resulting table has more than 15000 rows. We decided to store all the statistics for each country/region in a nested dictionary, placed in the column "properties".

## GADM regions identifiers (GID)
In the same two notebooks we also associated to each country/region its GID code. This procedure is immediate for data at the country level (the GID is the ISO3 code of the country), but it is not when considering regions. The region codes used in the IVS vary from country to country and they often do not match the GADM regions at a particular level. We manually matched the IVS region to one or more GADM codes only for the 35 most important countries (see borda count table) and for each country we only considered its most recent survey. The resulting dictionary can be found in the folder "/gid".\
Because of this our database contains the full IVS data aggregated by country and a subset of it (the most recent and important one) aggregated by region.

# TABLE SCHEMA

The SURVEYS table has the following columns:\

source |	varchar	| Data source of the survey \
wave |	varchar |	Wave period of the survey \
gid |	array	| Unique geographical ID, for more details see gadm.org \
country |	varchar |	English name for the country \
countrycode |	varchar |	ISO 3166-1 alpha-3 country codes \
adm_area_1 |	varchar |	Level-1 administrative country subdivision \
adm_area_2 |	varchar |	Level-2 administrative country subdivision \
adm_area_3 |	varchar |	Level-3 administrative country subdivision \
samplesize |	int |	Number of people that took part in the survey \
properties |	dict |	Dictionary containing the region/country statistics. \

The user must be aware that the dictionaries found in "properties" will have different structures depending on the source.   
