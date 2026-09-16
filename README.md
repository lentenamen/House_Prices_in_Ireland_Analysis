# House-Prices-in-Ireland

# Project Description
This repo will used to predict house prices in Ireland based off of their features and location.

## Dataset

- **Name:** PPR-ALL
- **Source:** [(https://www.propertypriceregister.ie/)](https://www.propertypriceregister.ie/)
- **Size:** 800K Rows, 11 Columns
- **Format:** CSV


Project Structure
``` text
House-Prices-in-Ireland/
│
├── data/
│   └── raw/
│       └── PPR-ALL.csv
│
├── notebooks/
│   └── main.ipynb
│
├── outputs/
│   └── national_price_trend.png
│
├── src/
│   ├── analysis.py
│   ├── data_loader.py
│   ├── main.py
│   ├── preprocessing.py
│   └── visualization.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Overview

This project uses raw property sale records from the Irish Property Price Register to explore:

How house prices have changed nationally over time
How Dublin's share of property sales compares to the rest of Ireland
Which areas (by Eircode routing key) have the highest median prices
Whether a simple linear regression model can predict sale price from property and location features

## Data Cleaning

The raw CSV is loaded and cleaned before analysis:

Columns renamed to consistent, lowercase, snake_case names (date, county, eircode, price, property_type, etc.)
date parsed from dd/mm/yyyy format, with year and month extracted
county names standardized (trimmed, lowercased)
price converted from formatted currency strings (e.g. "€350,000") to numeric values
Duplicate rows removed

## Analysis & Visualizations

National price trends: Median and mean price per year, plotted alongside year-over-year percentage change, with the post-2008 crash and COVID-19 periods highlighted.

Dublin vs. Rest of Ireland: An is_dublin flag is derived from the county column to compare:

Total and yearly sales volume between Dublin and the rest of the country
Dublin's share of national sales over time (line chart) and overall (pie chart)

Most expensive areas: Properties are grouped by Eircode routing key (first 3 characters of the Eircode) to find the areas with the highest median sale price, filtered to routing keys with at least 30 sales to avoid noise from small samples.

Price prediction: A linear regression model (scikit-learn) predicts sale price from county, year, and property_type (one-hot encoded). Extreme price outliers (top/bottom 1%) are trimmed before training. Model performance is evaluated using R² and Mean Absolute Error.

## Tech Stack
Python: pandas, NumPy
Visualization: Matplotlib, Seaborn
Modeling: scikit-learn (LinearRegression, train_test_split)

## Getting Started
Place the raw PPR CSV file at data/raw/PPR-ALL.csv
Install dependencies: pandas, numpy, matplotlib, seaborn, scikit-learn
Run main.ipynb from top to bottom