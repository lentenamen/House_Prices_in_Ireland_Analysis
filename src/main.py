from data_loader import load_data
from preprocessing import standardize
from analysis import analysis, regional_comparison, dublin_share, eircode_analysis, train_price_model
from visualization import visualisation1, visualisation2, visualisation3, visualisation4

def main():
    # Path to the raw dataset
    file_path = "data/raw/PPR-ALL.csv"

    # Load the data
    df = load_data(file_path)
    if df is None:
        print("Failed to load the data")
        return
    df = standardize(df)
    annual = analysis(df)
    visualisation1(annual)

    yearly_comparison = regional_comparison(df)
    visualisation2(yearly_comparison)

    yearly_comparison, overall_totals = dublin_share(df, yearly_comparison)
    visualisation3(yearly_comparison, overall_totals)

    eircode_stats = eircode_analysis(df)
    visualisation4(eircode_stats)

    train_price_model(df)


if __name__ == "__main__":
    main()