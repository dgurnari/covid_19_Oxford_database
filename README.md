# covid_19_Oxford_database

## USAGE
python wb_data_fetcher.py <indicators.csv>


<indicators.csv> must be a csv file with (at least) a column named "code"
elements of this column must be valid indicator codes that can be found at https://data.worldbank.org/indicator?tab=all
additional columns can be used to describe the indicators but are not read by the script.

the same code is available in the jupiter notebook wb_data_fetcher.ipynb

## <indicators.csv> example

code,description,type\
SP.POP.TOTL,Population total,Climate Change\
AG.SRF.TOTL.K2,Surface area (sq. km),Agriculture & Rural Development\

a bigger example can be found in "interesting_indicators.csv"

## what does the script do

wb_data_fetcher.py downloads the entire dataset "WDIData.csv" from http://databank.worldbank.org/data/download/WDI_csv.zip
slice it keeping only the the rows relative to the indicators in <indicators.csv> and for each row keeps only the most recent value and its year.

returns a csv file "wb_out.csv" with the following columns\
Country Name, Country Code, Indicator Name, Indicator Code, Most Recent Value, Year

Note: in the "WDIData.csv" dataset there are not only single countries but also groups of them such as Arab World and European Union. For the time being the script keeps them even if they cointain, in average, more NaNs. 




## what about the world bank APIs
Downloading the entire dataset seems to be the easiest way to go, but there are also API and a python wrapper
https://wbdata.readthedocs.io/en/stable/index.html
the wbdata.get_dataframe method returns takes as input a dictionary of indicators and returns a multi-index (country, year) pandas dataframe which makes the slicing more complicated
