import pandas as pd
import numpy as np

def standardize(df):
    df = df.rename(columns={
        "Date of Sale (dd/mm/yyyy)": "date",
        "Address": "address",
        "County": "county",
        "Eircode": "eircode",
        "Price (€)": "price",
        "Not Full Market Price": "not_full_market_price",
        "VAT Exclusive": "vat_exclusive",
        "Description of Property": "property_type",
        "Property Size Description": "property_size"
    })
    

    df["date"] = pd.to_datetime(df["date"],format="%d/%m/%Y",errors="coerce")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    df["county"] = df["county"].str.strip().str.lower()

    # Blank eircodes become proper missing values so dropna() catches them
    df["eircode"] = df["eircode"].str.strip().replace("", np.nan)

    df["price"] = pd.to_numeric(
        df["price"]
        .str.replace("€", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # --- Outlier Handling (Percentile Trimming) ---
    lower_percentile = df["price"].quantile(0.01)  # Bottom 1%
    upper_percentile = df["price"].quantile(0.99)  # Top 1%

    df = df[
        (df["not_full_market_price"].str.strip().str.title() == "No") &
        (df["price"] >= lower_percentile) &
        (df["price"] <= upper_percentile)
    ]

    df = df.drop_duplicates()

    return df