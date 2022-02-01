# ALT2 Project - Data Science
## _Colin Simon-Fellowes_

## Table of Contents
 - [1.0: Overview](#10-overview)
 - [1.1: Hypothesis](#11-hypothesis)
 - [1.2: Cleaning the Dataset](#12-cleaning-the-dataset)
 - [1.3: Visualizing the Data](#13-visualising-the-data)
 - [1.4: Interpreting the Data](#14-interpreting-the-data)
___

### 1.0 Overview

The goal of this project is to clean and visualise a given dataset using Python in order to examine an initial hypothesis about the relationship of any two components of the dataset. The 
[data](https://www.rsa.ie/road-safety/statistics/nct-statistics-and-annual-reviews)
used was taken from the Irish Road Safety Authority, and details the results of car safety tests for Irish cars by make, model and year manufactured.

### 1.1 Hypothesis

My initial hypothesis was relatively simple - that the age of a car is inversely proportional to its safety test pass percentage. The assumption behind it is equally straightforward – that cars decline in function as they age. To test this data I determined that I'd need to restructure the initial dataset to aggregate cars by age alone, and so this was the driving factor of the initial design of the project. 

### 1.2 Cleaning the Dataset

To clean the dataset I decided to write a [function](/src/data_analysis.py) (see *get_yrman_passpct()*) to take in a valid .xlsx file and aggregate its rows by year manufactured, returning a list of years manufactured, test pass percentage, and total vehicles.

I ran this function on all of the files (data from 2013-2020) and for each subtracted the year in which the data was taken to get the ages of the vehicles, and finally combinined them all into a
[.csv file](/src/data/clean/yrman-passpct.txt)
in which each row had the format (Year of Data, Age, Pass %, Total).

### 1.3 Visualising the Data

To visualise the relationship between age and pass percentage, I used the module
[plotly](https://plotly.com/python/),
which allows for easy, stylised, and interactive visualisation of data through python.

For the graph's appearance I analysed the type of data I was working with, and determined that the optimal chart type would be a multi-series line chart, as I wanted to represent a continuous progression between a series of known points.

I then read the data from my cleaned dataset, and for each year plotted a differently coloured line showing the relationship between vehicle age and test pass percentage for that year. I also averaged the age data between all of the datasets, and plotted that line too (see "AVG" series in graph)

This graph was saved as an HTML file, and can be viewed [here](https://ctsf1.github.io/data_sci/src/graphs/output.html)

### 1.4 Interpreting the Data
PauseChamp