#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


print("loading data")
data = pd.read_csv("input/Integrated_data.csv", low_memory = False)
print("data loaded")

# # Load up the list of variables we want to aggregate
variables = pd.read_csv("input/IVS_Variable_List.csv")
variables_to_keep = variables[variables.Included == 1].Name

data_subset = data.loc[: , data.columns.isin(variables_to_keep)].copy()

WVS_wave = pd.read_csv("input/WVS_wave.csv", index_col = "code").wave.to_dict()
EVS_wave = pd.read_csv("input/EVS_wave.csv", index_col = "code").wave.to_dict()

WVS_wave[-4] = ""
EVS_wave[-4] = ""

for key in WVS_wave:
    data_subset.loc[data_subset['S002'] == key, ['S002']] = WVS_wave[key]

for key in EVS_wave:
    data_subset.loc[data_subset['S002EVS'] == key, ['S002EVS']] = EVS_wave[key]

data_subset.S002 += data_subset.S002EVS

data_subset.drop(['S002EVS'], axis = 1, inplace = True)
data_subset.rename(columns={'S002':'Wave'}, inplace=True)

data_subset.loc[data_subset['S001'] == 1, ['S001']] = "EVS"
data_subset.loc[data_subset['S001'] == 2, ['S001']] = "WVS"

data_subset.rename(columns={'S001':'Survey'}, inplace=True)

data_subset.rename(columns={'S003':'Country Numeric'}, inplace=True)
data_subset.rename(columns={'X048':'Region Numeric'}, inplace=True)
data_subset.rename(columns={'S017':'Weight'}, inplace=True)


#######################################
# ## One-hot encoding

not_to_encode = ["Survey", "Wave", "Country Numeric", "Region Numeric", "Weight"] # are the variables we want to groupby and the weights (S017)

one_hot = pd.get_dummies(data=data_subset.loc[: , [c for c in data_subset.columns if c not in not_to_encode] ],
                           columns=[c for c in data_subset.columns if c not in not_to_encode])

# ## Multiply by the weights
weighted_one_hot = one_hot.mul(data_subset["Weight"], axis=0).copy()



##################################################################
# # Groupby Country

# ### For country statistics we can correct the numbers using S007
weighted_one_hot["Survey"] = data_subset["Survey"]
weighted_one_hot["Wave"] = data_subset["Wave"]
weighted_one_hot["Country Numeric"] = data_subset["Country Numeric"]

grouped_by_country = weighted_one_hot.groupby(["Survey", "Wave", "Country Numeric"]).mean().copy()
grouped_by_country["Sample Size"] = weighted_one_hot.groupby(["Survey", "Wave", "Country Numeric"]).size()


# ### Lets add the country names
country_ISO = pd.read_csv("input/ISO_3611.csv", index_col = "numeric")

names = []
ISO3 = []

for idx in grouped_by_country.index:
    names.append(country_ISO.loc[idx[2], "Country"])
    ISO3.append(country_ISO.loc[idx[2], "alpha-3"])


grouped_by_country["Country Name"] = names
grouped_by_country["Country ISO3"] = ISO3

# ### Flat the index
grouped_by_country = grouped_by_country.reset_index()

# ### Move the last columns to the front
columns = list(grouped_by_country.columns)
grouped_by_country = grouped_by_country[columns[:3] + columns[-2:] + [columns[-3]] + columns[3:-3]]

# ### Save to csv

grouped_by_country.to_csv("out/IVS_grouped_by_country.csv", index = False, encoding = 'utf-16')
print("saved to {}".format("out/IVS_grouped_by_country.csv"))







#############################################################
# # Groupby Country and Region

# ### For regional aggregation we can not use the weighted answers

one_hot["Survey"] = data_subset["Survey"]
one_hot["Wave"] = data_subset["Wave"]
one_hot["Country Numeric"] = data_subset["Country Numeric"]
one_hot["Region Numeric"] = data_subset["Region Numeric"]


grouped_by_country_region = one_hot.groupby(["Survey", "Wave", "Country Numeric", "Region Numeric"]).mean().copy()
grouped_by_country_region["Sample Size"] = one_hot.groupby(["Survey", "Wave", "Country Numeric", "Region Numeric"]).size()


# ### Add the country and region names
region_codes = pd.read_csv("input/Region_codes.csv", index_col="Code")

region_name = []
r_names = []
r_ISO3 = []


for idx in grouped_by_country_region.index:
    region_name.append(region_codes.loc[idx[3], "Region"])
    r_names.append(country_ISO.loc[idx[2], "Country"])
    r_ISO3.append(country_ISO.loc[idx[2], "alpha-3"])


grouped_by_country_region["Country Name"] = r_names
grouped_by_country_region["Country ISO3"] = r_ISO3
grouped_by_country_region["Region Name"] = region_name


# ### Flat the index

grouped_by_country_region = grouped_by_country_region.reset_index()

# ### Move the last column to the front
columns_r = list(grouped_by_country_region.columns)

grouped_by_country_region = grouped_by_country_region[columns_r[:3] + columns_r[-2:-1]
                                                      + [columns_r[3]]+ [columns_r[-1]]
                                                      + [columns_r[-4]]+ columns_r[4:-4]]


# ### Save to csv


grouped_by_country_region.to_csv("out/IVS_grouped_by_country_region.csv", index = False, encoding = 'utf-16')
print("saved to {}".format("out/IVS_grouped_by_country_region.csv"))
