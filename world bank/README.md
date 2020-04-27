# covid_19_Oxford_database

## USAGE
python wb_data_fetcher.py <indicators.csv> [optional <dataset.zip>]


<indicators.csv> must be a csv file with (at least) a column named "code" and another named "category".\
Elements of the "code" column must be valid indicator codes that can be found at https://data.worldbank.org/indicator?tab=all .\
Elements in the "category" column will be used to divide the output file in subsets.\
Additional columns can be used to describe the indicators but are not read by the script.

By default the script downloads the entire dataset "WDIData.csv" from http://databank.worldbank.org/data/download/WDI_csv.zip .\
If a second argument is provided the dataset will be loaded locally from the path <dataset.zip> .


## <indicators.csv> example

code,description,category\
SP.POP.TOTL,Population total,Climate Change\
AG.SRF.TOTL.K2,Surface area (sq. km),Agriculture & Rural Development

a bigger example can be found in "interesting_indicators.csv"

## what does the script do

wb_data_fetcher.py load the entire dataset "WDIData.csv" either from the World Bank website or from a local file.
Slice it keeping only the the rows relative to the indicators in <indicators.csv> and for each row keeps only the most recent value and its year.

Returns a csv file "wb_out_FULL.csv" with the following columns\
Country Name, Country Code, Indicator Name, Indicator Code, Most Recent Value, Year

and similar subset of it named "wb_out_{CATEGORY}.csv" which contain only the indicators of a certain CATEGORY.

Note: in the "WDIData.csv" dataset there are not only single countries but also groups of them such as Arab World and European Union. For the time being the script keeps them even if they cointain, in average, more NaNs.




## what about the world bank APIs
Downloading the entire dataset seems to be the easiest way to go, but the Worlds Bank has its own API to query the dataset. Moreover there is a python wrapper of such APIs
https://wbdata.readthedocs.io/en/stable/index.html
the wbdata.get_dataframe method returns takes as input a dictionary of indicators and returns a multi-index (country, year) pandas dataframe which makes the slicing more complicated
