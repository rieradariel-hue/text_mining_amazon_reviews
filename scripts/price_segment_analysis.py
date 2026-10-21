from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


SAMPLE_PATH = Path("data/processed/all_beauty_sample_100k.csv")
META_PATH = Path("data/raw/meta_All_Beauty.jsonl")
OUTPUT_DIR = Path("outputs")



def load_priced_reviews() -> pd.DataFrame:
    """Koppla recensioner till pris via parent_asin (m:1) och behåll rader med pris."""
    reviews = pd.read_csv(SAMPLE_PATH, keep_default_na=False)
    meta = pd.read_json(META_PATH, lines=True)[["parent_asin", "price"]]

    #  Implementerar "många-till-en" och stoppar körningen om metadatan har dubbletter
    joined = reviews.merge(meta, on="parent_asin", how="left", validate="m:1")
    return joined.dropna(subset=["price"]).copy()


def add_price_segment(priced: pd.DataFrame) -> pd.DataFrame:
    """Dela priset i tre lika stora grupper (tertiler)."""
    priced["segment"] = pd.qcut(priced["price"], 3, labels=["low", "mid", "high"])
    return priced


def sentiment_share(priced: pd.DataFrame) -> pd.DataFrame:
    """Andel (%) av varje sentiment inom varje prissegment."""
    counts = pd.crosstab(priced["segment"], priced["sentiment"])
    return (counts.div(counts.sum(axis=1), axis=0) * 100).round(1)


def plot_share(share: pd.DataFrame) -> None:
    """Spara stapeldiagram över sentiment per prissegment."""
    ax = share.plot(kind="bar", rot=0)
    ax.set_xlabel("Price segment")
    ax.set_ylabel("Share (%)")
    ax.set_title("Sentiment share by price segment")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sentiment_by_price_segment.png")
    plt.close()    # Stänger denna figur så att nästa diagram har en fresh start


def average_rating(priced: pd.DataFrame) -> pd.Series:
    """Medelbetyg per prissegment."""
    return priced.groupby("segment", observed=True)["rating"].mean().round(2)


def plot_average_rating(avg: pd.Series) -> None:
    """Spara stapeldiagram över medelbetyg per prissegment."""
    ax = avg.plot(kind="bar", color="steelblue", rot=0)
    ax.set_title("Average rating by price segment")
    ax.set_xlabel("Price segment")
    ax.set_ylabel("Average rating (1-5)")
    ax.set_ylim(1, 5)      # Betyg från 1 till 5
    for i, value in enumerate(avg):
        ax.text(i, value + 0.05, str(value), ha="center")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "average_rating_by_segment.png")
    plt.close()


def extreme_comparison(priced: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Sentimentandel (%) för billigaste och dyraste 10 % av priserna."""
    low_limit = priced["price"].quantile(0.10)
    high_limit = priced["price"].quantile(0.90)

    #  Tar ut två ytterkanterna och märkerar dem
    cheapest = priced[priced["price"] <= low_limit].assign(group="cheapest 10%")
    priciest = priced[priced["price"] >= high_limit].assign(group="priciest 10%")
    extremes = pd.concat([cheapest, priciest])

    #  % per grupp så att gruppstorleken inte påverkar jämförelsen
    share = pd.crosstab(extremes["group"], extremes["sentiment"], normalize="index") * 100
    return share.round(1), extremes["group"].value_counts()


def plot_extremes(share: pd.DataFrame) -> None:
    """Spara staplat diagram för ytterkanterna."""
    ax = share.plot(kind="bar", stacked=True, rot=0)
    ax.set_title("Sentiment: cheapest vs priciest 10%")
    ax.set_xlabel("")
    ax.set_ylabel("Share (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sentiment_extremes.png")
    plt.close()


def main() -> None:
    #  Skapar output mapp först, där filerna ska sparas
    
    OUTPUT_DIR.mkdir(exist_ok=True)

    priced = add_price_segment(load_priced_reviews())

    #  1a del: sentiment andel per prissegment
    share = sentiment_share(priced)
    share.to_csv(OUTPUT_DIR / "sentiment_share_by_segment.csv")
    print(share)
    plot_share(share)

    # 2a del: medelbetyg per prissegment
    avg = average_rating(priced)
    avg.to_csv(OUTPUT_DIR / "average_rating_by_segment.csv")
    print(avg)
    plot_average_rating(avg)

    # 3e del: billigaste mot dyraste 10%
    extremes_share, extremes_counts = extreme_comparison(priced)
    extremes_share.to_csv(OUTPUT_DIR / "sentiment_extremes.csv")
    print(extremes_share)
    print(extremes_counts)
    plot_extremes(extremes_share)


if __name__ == "__main__":
    main()