# covid_19_Oxford_database
# COUNTRY STATISTICS

The country_statistics table contains data from two different source: the Word Bank and the Integrated Value Survey. The original dataset are very different so a bit of preprocessing is needed.


# WORD BANK
## Fetcher
We provide a python script to download and slice the entire Word Bank dataset. It can be executed with the following command \

python wb_data_fetcher.py <indicators.csv> [optional <dataset.zip>]

<indicators.csv> must be a csv file with (at least) a column named "code" and another named "category".\
Elements of the "code" column must be valid indicator codes that can be found at https://data.worldbank.org/indicator?tab=all .\
Elements in the "category" column will be used to divide the output file in subsets.\
Additional columns can be used to describe the indicators but are not read by the script.

By default the script downloads the entire dataset "WDIData.csv" from http://databank.worldbank.org/data/download/WDI_csv.zip .\
If a second argument is provided the dataset will be loaded locally from the path <dataset.zip> .


## what does the script do

wb_data_fetcher.py loads the entire dataset "WDIData.csv" either from the World Bank website or from a local file.
Slice it keeping only the the rows relative to the indicators in <indicators.csv> and for each row keeps only the most recent value and its year.

Returns a csv file "wb_out_FULL.csv" with the following columns\
Country Name, Country Code, Indicator Name, Indicator Code, Most Recent Value, Year

and similar subset of it named "wb_out_{CATEGORY}.csv" which contain only the indicators of a certain CATEGORY.

Note: in the "WDIData.csv" dataset there are not only single countries but also groups of them such as Arab World and European Union. Since thoose region do not have a GID we drop them.


## what about the world bank APIs
Downloading the entire dataset seems to be the easiest way to go, but the Worlds Bank has its own API to query the dataset. Moreover there is a python wrapper of such APIs
https://wbdata.readthedocs.io/en/stable/index.html
the wbdata.get_dataframe method returns takes as input a dictionary of indicators and returns a multi-index (country, year) pandas dataframe which makes the slicing more complicated





# Integrated Value Survey

## About the Integrated Values Survey and data fetching
The Integrayed Value Survey dataset is obtained by merging together six waves of the World Value Survey with four waves of the European Value Survey.\
https://europeanvaluesstudy.eu/methodology-data-documentation/previous-surveys-1981-2008/integrated-values-surveys-1981-2014/

Since this integrated dataset is not directly available we personally merged it folowing the official guidelines. Our version can be found at
https://drive.google.com/drive/folders/1ug6_ndeEi4OhmAZJeXiZmG7BO6T5bPX9?usp=sharing
and contains 1430 variables and 513529 observations.

## Variables Processing and Aggregation
The Integrated_Values_Survey_aggregator.ipynb notebook aggregates the answers found in the Integrated Values Survey Dataset.

We considered only a subset of all the questions found in the surveys, this list can be found in the file IVS_Variable_List.cvs

We aim to provide two different levels of aggregation:
- by Survey, Wave and Country;
- by Survey, Wave, Country and local region.

Before being aggregate each individual answer is one-hot encoded. \
For each answer in the dataset, a weight is available to compensate for small deviations in the sample at the country level.\
http://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=WEIGHT \
When aggregating at the country level we choosed to rescale each answer, when aggregating at the region level we choosed not to. \
We used the aritmetic mean as the aggregating function, since each answer was one hot encoded we can interpret the resulting values as frequencies.

## PROPERTIES DICTIONARY
As an effect of the one hot encoding the resulting table has more than 15000 rows. We decided to store all the statistics for each country/region in a nested dictionary, placed in the column "properties".
The code for creating such dictionaries can be found in the notebooks \
add_properties_groupedby_country.ipynb\
add_properties_groupedby_region.ipynb\

## GADM regions identifiers (GID)
In the same two notebooks we also associated to each country/region its GID code. This procedure is immediate for data at the country level (the GID is the ISO3 code of the country), but it is not when considering regions. The region codes used in the IVS vary from country to country and they often do not match the GADM regions at a particular level. We manually matched the IVS region to one or more GADM codes only for the 35 most important countries (see borda count table) and for each country we only considered its most recent survey. The resulting dictionary can be found in the folder "gid".\
Because of this our database contains the full IVS data aggregated by country and a subset of it (the most recent and important one) aggregated by region.

# COUNTRY STATISTICS TABLE
In order to be able to insert in the same table data from WB and IVS we aggregated by country also the WB data. For each country we constructed a "properties" dictionary that contains all its indicators.\
The code for this counstruction can be found in unify_country_stats_table.ipynb \

The country_statistics table has the following columns:\

| source | year| country | countrycode | adm_level | gid | samplesize | properties | \

- source: can be WVS, EVS, WB;
- year: is 2020 for WB data, the wave period for IVS data;
- country: name of the country in English;
- countrycode: alpha-3 ISO code of the country;
- adm_level: level of the aggregation, 0 for WB and IVS by country, 1 for IVS by region;
- gid: array of GADM identifiers for the considered country/region;
- samplesize: number of questions for IVS data, -1 for WB;
- properties: the dictionaries described above. \

The user must be aware that the dictionaries found in "properties" will have different structures depending on the source.   
