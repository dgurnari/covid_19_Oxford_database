# covid_19_Oxford_database
# Integrated Value Survey aggregator

## INFO
The Integrated_Values_Survey_aggregator.py script aggregates the answers found in the Integrated Values Survey Dataset.

## About the Integrated Values Survey
The Integrayed Value Survey dataset is obtained by merging together six waves of the World Value Survey with four waves of the European Value Survey.\
https://europeanvaluesstudy.eu/methodology-data-documentation/previous-surveys-1981-2008/integrated-values-surveys-1981-2014/

Since this integrated dataset is not directly available we personally merged it folowing the official guidelines. Our version can be found at
https://drive.google.com/drive/folders/1ug6_ndeEi4OhmAZJeXiZmG7BO6T5bPX9?usp=sharing
and contains 1430 variables and 513529 observations.

## Variables Processing and Aggregation
We aim to provide two different levels of aggregation:
- by Survey, Wave adn Country;
- by Survey, Wave, Country and local region.

Before being aggregate each individual answer is one-hot encoded. \
For each answer in the dataset, a weight is available to compensate for small deviations in the sample at the country level.\
http://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=WEIGHT \
When aggregating at the country level we choosed to rescale each answer, when aggregating at the region level we choosed not to. \
We used the aritmetic mean as the aggregating function, since each answer was one hot encoded we can interpret the resulting values as frequencies.
