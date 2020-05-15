import numpy as np
import pandas as pd

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

from sys import argv





def download_WDIdata_to_df(url):
    print("Dowloading")
    resp = urlopen(zip_url)
    zipfile = ZipFile(BytesIO(resp.read()))
    print("Downloaded")

    print("Loading into a pandas dataframe")
    data = pd.read_csv(zipfile.open('WDIData.csv'))
    print("Dataframe created")

    return data



def load_local_WDIdata(zip_path):
    print("loading data from ", zip_path)
    zipfile = ZipFile(zip_path)
    data = pd.read_csv(zipfile.open('WDIData.csv'))
    print("Dataframe created")

    return data




if __name__ == "__main__":
    if len(argv) < 2:
        raise ValueError('please specify the codes csv file')

    CODES_PATH = argv[1]

    DOWNLOAD_ZIP = True

    # if a third argument is provided, do not download the zip file
    # but load it locally from the provided path

    if len(argv) == 3:
        DOWNLOAD_ZIP = False
        ZIP_PATH = argv[2]


    if DOWNLOAD_ZIP:
        zip_url = "http://databank.worldbank.org/data/download/WDI_csv.zip"
        # it can take some minutes
        wb_df = download_WDIdata_to_df(zip_url)

    else:
        wb_df = load_local_WDIdata(ZIP_PATH)






    # remove the last column (always empty)
    wb_df.drop("Unnamed: 64", axis=1, inplace=True)

    # load the indicators we are interested in
    interesting_indicators = pd.read_csv(CODES_PATH)
    data = wb_df.loc[wb_df["Indicator Code"].isin(interesting_indicators["code"])].copy()

    # create a dictionary with the various categories of indicators
    category_dict = {}
    for index, row in interesting_indicators.iterrows():
        category_dict.setdefault(row.category, []).append(row.code)

    # the last column name is the most recent year
    most_recent_year = int(data.columns[-1])

    # creates two additional columns
    data.loc[:, "Most Recent Value"] = np.nan
    data.loc[:, "Year"] = np.nan

    # for each row, find the most recent non NaN measure
    for year in range(most_recent_year, 1959, -1):
        if data["Most Recent Value"].isnull().values.any():
            data.loc[data["Most Recent Value"].isnull(), "Year"] = int(year)
            data.loc[: ,"Most Recent Value"].fillna(data[str(year)], inplace=True)
        else:
            break

    # drop all the colums with years
    cols_to_drop = [str(year) for year in range(1960, most_recent_year+1)]

    data_recent = data.drop(cols_to_drop, axis=1)

    # load the full list of countries with a GID
    gid_list = pd.read_csv("gid/admn_0.csv")

    # consider only the rows with a valid GID
    data_to_output = data_recent[data_recent["Country Code"].isin(gid_list["countrycode"])].copy()

    # add a GID column
    data_to_output["GID"] = data_to_output["Country Code"]

    # save the full table to csv
    data_to_output.to_csv("out/wb_out_FULL.csv", index=False, na_rep = "NaN")
    print("saved to data/wb_out.csv")

    # for each category
    # saves rows with indicators in that category
    for key in category_dict:
        data_subset = data_to_output.loc[data_to_output["Indicator Code"].isin(category_dict[key])].copy()
        data_subset.to_csv("out/wb_out_{}.csv".format(key), index=False, na_rep = "NaN")

    print("subsets saved")
