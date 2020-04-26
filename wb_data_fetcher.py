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





if __name__ == "__main__":
    if len(argv) < 2:
        raise ValueError('please specify the codes csv file')

    CODES_PATH = argv[1]

    zip_url = "http://databank.worldbank.org/data/download/WDI_csv.zip"

    # it can take some minutes
    wb_df = download_WDIdata_to_df(zip_url)

    # remove the last column (always empty)
    wb_df.drop("Unnamed: 64", axis=1, inplace=True)

    # load the indicators we are interested in
    interesting_indicators = pd.read_csv(CODES_PATH)
    data = wb_df.loc[wb_df["Indicator Code"].isin(interesting_indicators["code"])].copy()

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

    data_to_output = data.drop(cols_to_drop, axis=1)

    #save to csv

    data_to_output.to_csv("wb_out.csv", index=False, na_rep = "NaN")
    print("saved to wb_out.csv")
