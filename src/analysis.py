import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def analysis(df):
    print(f'Rows:     {len(df):,}')
    print(f'Columns:  {df.shape[1]}')
    print(f'Date range: {df["date"].min().date()} -> {df["date"].max().date()}')

    labels = ['Min', '10th %ile', '25th %ile', 'Median', '75th %ile', '90th %ile', 'Max']
    values = np.percentile(df['price'], [0, 10, 25, 50, 75, 90, 100])

    print('National price distribution (all years):')
    print('-' * 35)
    for l, v in zip(labels, values):
        print(f'  {l} €{v:.0f}')
    print(f'\n  Mean        €{df["price"].mean():.0f}')
    print(f'  Std dev     €{df["price"].std():.0f}')

    annual = df.groupby('year').agg(
    median_price=('price', 'median'),
    mean_price=('price', 'mean'),
    total_sales=('price', 'count'),
    total_value=('price', 'sum')
    ).reset_index()

    annual['yearly_percentage_change'] = annual['median_price'].pct_change() * 100

    return annual


def regional_comparison(df):
    df["is_dublin"] = df["county"] == "dublin"
    print(df["is_dublin"].head())
    print(df["is_dublin"].sum())

    yearly_comparison = (
        df.groupby(["year", "is_dublin"])
        .size()
        .reset_index(name="sales_count")
    )
    yearly_comparison["region"] = yearly_comparison["is_dublin"].map(
        {True: "Dublin", False: "Rest of Ireland"}
    )

    return yearly_comparison


def dublin_share(df, yearly_comparison):
    yearly_comparison = yearly_comparison.copy()
    yearly_comparison["total"] = yearly_comparison.groupby("year")["sales_count"].transform("sum")
    yearly_comparison["pct_of_total"] = yearly_comparison["sales_count"] / yearly_comparison["total"] * 100

    overall_totals = df["is_dublin"].value_counts().rename({True: "Dublin", False: "Rest of Ireland"})

    return yearly_comparison, overall_totals


def eircode_analysis(df):
    df["eircode_routing_key"] = df["eircode"].str[:3]

    eircode_stats = (
        df.dropna(subset=["eircode_routing_key"])
        .groupby("eircode_routing_key")
        .agg(median_price=("price", "median"), sales_count=("price", "count"))
        .query("sales_count >= 30")  # drop routing keys with too few sales to be meaningful
        .sort_values("median_price", ascending=False)
    )

    print(f"Most expensive eircode: {eircode_stats.index[0]} — median €{eircode_stats['median_price'].iloc[0]:,.0f}")

    return eircode_stats


def train_price_model(df):
    # Check the county data
    print(df["county"].head())

    # Keep only rows with the information needed for the model
    model_df = df.dropna(
        subset=["price", "county", "year", "property_type"]
    ).copy()

    # Cap extreme prices so they don't dominate the regression
    lower, upper = model_df["price"].quantile([0.01, 0.99])

    model_df = model_df[
        (model_df["price"] >= lower) &
        (model_df["price"] <= upper)
    ]

    # One-hot encode categorical variables
    # drop_first=True creates a reference category
    X = pd.get_dummies(
        model_df[["county", "year", "property_type"]],
        columns=["county", "property_type"],
        drop_first=True
    )

    # Target variable
    y = model_df["price"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Create and train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Display model coefficients
    coefficients = pd.DataFrame({
        "Feature": X.columns,
        "Coefficient (€)": model.coef_
    })

    coefficients = (
        coefficients
        .sort_values(by="Coefficient (€)", ascending=False)
        .reset_index(drop=True)
    )

    print("\nTop 10 features by coefficient:")
    print(coefficients.head(10))

    # Model performance
    print(f"\nR² score: {r2_score(y_test, y_pred):.3f}")
    print(
        f"Mean Absolute Error: "
        f"€{mean_absolute_error(y_test, y_pred):,.0f}"
    )

    return model, coefficients