#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# # Integrated Data
print("loading the data - it can take a while")
data = pd.read_csv("input/Integrated_data.csv", low_memory = False)
print("loaded")

# # Load up the list of variables we want to aggregate
variables = pd.read_csv("input/IVS_Variable_List.csv")
variables_to_keep = variables[variables.Included == 1].Name
data_subset = data.loc[: , data.columns.isin(variables_to_keep)].copy()


# ## One-hot encoding
not_to_encode = ["S003", "S020", "S017", "X048"] # are the variables we want to groupby and the weights (S017)
one_hot = pd.get_dummies(data=data_subset.loc[: , [c for c in data_subset.columns if c not in not_to_encode] ],
                           columns=[c for c in data_subset.columns if c not in not_to_encode])


# ## Multiply by the weights
weighted_one_hot = one_hot.mul(data_subset.S017, axis=0).copy()

######################################################
# ################ Groupby Country ###################
######################################################
weighted_one_hot["S003"] = data_subset["S003"]
weighted_one_hot["Year"] = data_subset["S020"]
grouped_by_country = weighted_one_hot.groupby(["S003", "Year"]).mean().copy()



# ### Lets add the country names
country_ISO = pd.read_csv("input/ISO_3611.csv", index_col = "numeric")

names = []
ISO3 = []

for idx in grouped_by_country.index:
    names.append(country_ISO.loc[idx[0], "Country"])
    ISO3.append(country_ISO.loc[idx[0], "alpha-3"])

grouped_by_country["Country Name"] = names
grouped_by_country["Country ISO3"] = ISO3


# ### Move the last columns to the front
columns = list(grouped_by_country.columns)
grouped_by_country = grouped_by_country[columns[-2:] + columns[:-2]]


# ### Flat the index
grouped_by_country = grouped_by_country.reset_index()
grouped_by_country.drop("S003", axis = 1, inplace = True)

# ### Save to csv
print("Saving to {}".format("out/IVS_grouped_by_country.csv"))
grouped_by_country.to_csv("out/IVS_grouped_by_country.csv", index = False)




######################################################
###### Groupby Country and Region ####################
######################################################
weighted_one_hot["X048"] = data_subset["X048"]
grouped_by_country_region = weighted_one_hot.groupby(["S003", "Year", "X048"]).mean().copy()


# ### Add the country and region names
region_codes = pd.read_csv("input/Region_codes.csv", index_col="Code")

region_name = []
r_names = []
r_ISO3 = []

for idx in grouped_by_country_region.index:
    region_name.append(region_codes.loc[idx[2], "Region"])
    r_names.append(country_ISO.loc[idx[0], "Country"])
    r_ISO3.append(country_ISO.loc[idx[0], "alpha-3"])

grouped_by_country_region["Country Name"] = r_names
grouped_by_country_region["Country ISO3"] = r_ISO3
grouped_by_country_region["Region"] = region_name


# ### Move the last column to the front
columns_r = list(grouped_by_country_region.columns)
grouped_by_country_region = grouped_by_country_region[columns_r[-3:] + columns[:-3]]
grouped_by_country_region = grouped_by_country_region.reset_index()
grouped_by_country_region
grouped_by_country_region.drop(["S003", "X048"], inplace = True, axis = 1)



# Save
print("Saving to {}".format("out/IVS_grouped_by_country_region.csv"))
grouped_by_country_region.to_csv("out/IVS_grouped_by_country_region.csv", index = False)
