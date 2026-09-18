import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def visualisation1(annual): 
    ACCENT = "#2b5c8f"  # Main median line color (e.g., steel blue)
    BLUE = "#1f77b4"  # Mean line color
    GREEN = "#2ca02c"  # Positive YoY percentage bars
    RED = "#d62728"  # Negative YoY percentage bars & post-crash highlight
    PURPLE = "#9467bd"  # COVID-19 highlight

    sns.set_theme(style="whitegrid", palette="muted")

    fig, axes = plt.subplots(
        2, 1, figsize=(14, 10), gridspec_kw={"height_ratios": [2, 1]}
    )

    # --- Top Plot: Price Trends using sns.lineplot ---
    ax = axes[0]

    # Line plots for Median and Mean
    sns.lineplot(
        data=annual,
        x="year",
        y="median_price",
        ax=ax,
        color=ACCENT,
        linewidth=2.5,
        marker="o",
        markersize=6,
        label="Median",
    )

    sns.lineplot(
        data=annual,
        x="year",
        y="mean_price",
        ax=ax,
        color=BLUE,
        linewidth=1.5,
        linestyle="--",
        marker="s",
        markersize=4,
        label="Mean",
    )

    # Fill under the line (uses Matplotlib as Seaborn lineplot doesn't have a fill_between parameter)
    ax.fill_between(
        annual["year"], annual["median_price"], alpha=0.15, color=ACCENT
    )

    # Data Point Annotations
    for _, row in annual.iterrows():
        ax.annotate(
            f'€{row["median_price"]/1000:.0f}k',
            (row["year"], row["median_price"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=8,
            color=ACCENT,
        )

    # Highlight Spans
    ax.axvspan(2010, 2012.5, alpha=0.07, color=RED, label="Post-crash trough")
    ax.axvspan(2020, 2020.9, alpha=0.07, color=PURPLE, label="COVID-19")

    ax.set_title(
        "Irish Residential Property — National Median & Mean Sale Price", pad=12
    )
    ax.set_ylabel("Sale Price")
    ax.legend(framealpha=0.15)


    # --- Bottom Plot: YoY % Change using sns.barplot ---
    ax2 = axes[1]
    annual_clean = annual.copy()
    annual_clean["yearly_percentage_change"] = annual_clean["yearly_percentage_change"].fillna(0)

    # Seaborn barplot allows hue assignment for custom positive/negative colors
    sns.barplot(
        data=annual_clean,
        x="year",
        y="yearly_percentage_change",
        hue=annual_clean["yearly_percentage_change"] >= 0,
        palette={True: GREEN, False: RED},
        ax=ax2,
        legend=False,
        alpha=0.8,
    )

    ax2.axhline(0, color="#555", linewidth=0.8)
    ax2.set_title("Year-on-Year % Change in Median Price", pad=8)
    ax2.set_xlabel("")
    ax2.set_ylabel("")


    # --- Formatting Tick Labels directly from Matplotlib values ---
    fig.canvas.draw()

    # Format Y-Axis Labels
    yticks1 = ax.get_yticks()
    ax.set_yticklabels([f"€{val/1000:.0f}k" for val in yticks1])

    yticks2 = ax2.get_yticks()
    ax2.set_yticklabels([f"{val:+.1f}%" for val in yticks2])


    plt.tight_layout(pad=2)
    plt.savefig(
        "outputs/images/national_price_trend.png", dpi=150, bbox_inches="tight", facecolor="#0f1117"
    )
    plt.show()


def visualisation2(yearly_comparison):
    ACCENT = "#2b5c8f"
    BLUE = "#1f77b4"
    RED = "#d62728"
    PURPLE = "#9467bd"

    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=yearly_comparison,
        x="year",
        y="sales_count",
        hue="region",
        palette={"Dublin": ACCENT, "Rest of Ireland": BLUE},
        linewidth=2.5,
        marker="o",
        markersize=6,
    )

    # Highlight Spans
    plt.axvspan(2010, 2012.5, alpha=0.07, color=RED, label="Post-crash trough")
    plt.axvspan(2020, 2020.9, alpha=0.07, color=PURPLE, label="COVID-19")

    plt.title("Property Sales Over Time: Dublin vs Rest of Ireland")
    plt.ylabel("Number of Sales")
    plt.xlabel("Year")
    plt.legend(title="")
    plt.tight_layout()
    plt.savefig("outputs/images/Property Sales Over time in Dublin vs Rest of Ireland.png")
    plt.show()


def visualisation3(yearly_comparison, overall_totals):
    ACCENT = "#2b5c8f"
    BLUE = "#1f77b4"

    fig, axes = plt.subplots(1, 2, figsize=(16, 6), gridspec_kw={"width_ratios": [2, 1]})

    # --- Left: line chart over time ---
    sns.lineplot(
        data=yearly_comparison,
        x="year",
        y="pct_of_total",
        hue="region",
        palette={"Dublin": ACCENT, "Rest of Ireland": BLUE},
        linewidth=2.5,
        marker="o",
        ax=axes[0],
    )
    axes[0].set_title("Dublin's Share of National Property Sales Over Time")
    axes[0].set_ylabel("% of Total Sales")
    axes[0].set_xlabel("Year")
    axes[0].legend(title="")

    # --- Right: pie chart, overall total ---
    axes[1].pie(
        overall_totals.values,
        labels=overall_totals.index,
        autopct="%1.1f%%",
        colors=[ACCENT, BLUE],
        startangle=90,
    )
    axes[1].set_title("Overall Share (All Years)")

    plt.tight_layout()
    plt.savefig("outputs/images/Dublin_Share_Combined.png")
    plt.show()


def visualisation4(eircode_stats):
    ACCENT = "#2b5c8f"

    top15 = eircode_stats.head(15)

    plt.figure(figsize=(10, 7))
    sns.barplot(x=top15["median_price"], y=top15.index, color=ACCENT)
    plt.title("Top 15 Most Expensive Eircodes (Median Price)")
    plt.xlabel("Median Price (€)")
    plt.ylabel("Eircode")
    plt.tight_layout()
    plt.savefig("outputs/images/Most Expensive Eircodes.png")
    plt.show()