from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = Path("data/raw/All_Beauty.jsonl")
PROCESSED_DATA_DIR = Path("data/processed")

CLEANED_DATA_PATH = PROCESSED_DATA_DIR / "all_beauty_cleaned.csv"
SAMPLE_DATA_PATH = PROCESSED_DATA_DIR / "all_beauty_sample_100k.csv"

SAMPLE_SIZE = 100_000
RANDOM_STATE = 42


def assign_sentiment(rating: int) -> str:
    """Convert Amazon star ratings to sentiment labels."""
    if rating <= 2:
        return "negative"
    if rating == 3:
        return "neutral"
    return "positive"


def load_reviews() -> pd.DataFrame:
    """Load the raw All_Beauty review dataset."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Raw data file not found at {RAW_DATA_PATH}")
    return pd.read_json(RAW_DATA_PATH, lines=True)


def clean_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    """Clean review data and create sentiment labels."""
    cleaned_reviews = reviews.copy()

    valid_ratings = [1, 2, 3, 4, 5]

    if not set(cleaned_reviews["rating"].unique()).issubset(valid_ratings):
        raise ValueError(
            "Unexpected rating values found. Expected only 1, 2, 3, 4, or 5."
        )

    cleaned_reviews["sentiment"] = cleaned_reviews["rating"].apply(assign_sentiment)

    # Remove empty or whitespace-only review texts
    cleaned_reviews = cleaned_reviews[cleaned_reviews["text"].str.strip().ne("")].copy()

    # Remove exact duplicate reviews
    duplicate_columns = [
        "user_id",
        "asin",
        "rating",
        "title",
        "text",
        "timestamp",
    ]

    cleaned_reviews = cleaned_reviews.drop_duplicates(subset=duplicate_columns).copy()

    # Keep only columns needed later in the project
    cleaned_reviews = cleaned_reviews[
        [
            "rating",
            "title",
            "text",
            "asin",
            "parent_asin",
            "sentiment",
        ]
    ].copy()

    return cleaned_reviews.reset_index(drop=True)


def create_development_sample(cleaned_reviews: pd.DataFrame) -> pd.DataFrame:
    """Create reproducible sample while preserving sentiment distribution."""
    sample, _ = train_test_split(
        cleaned_reviews,
        train_size=SAMPLE_SIZE,
        stratify=cleaned_reviews["sentiment"],
        random_state=RANDOM_STATE,
    )

    return sample.reset_index(drop=True)


def main() -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    reviews = load_reviews()
    cleaned_reviews = clean_reviews(reviews)
    development_sample = create_development_sample(cleaned_reviews)

    expected_columns = [
        "rating",
        "title",
        "text",
        "asin",
        "parent_asin",
        "sentiment",
    ]

    if set(development_sample.columns) != set(expected_columns):
        raise ValueError("Development sample has unexpected columns.")

    if len(development_sample) != SAMPLE_SIZE:
        raise ValueError(
            f"Expected development sample size {SAMPLE_SIZE}, got {len(development_sample)}."
        )

    cleaned_reviews.to_csv(CLEANED_DATA_PATH, index=False)
    development_sample.to_csv(SAMPLE_DATA_PATH, index=False)

    print(f"Raw reviews: {len(reviews):,}")
    print(f"Cleaned reviews: {len(cleaned_reviews):,}")
    print(f"Development sample: {len(development_sample):,}")

    print("\nSample sentiment distribution:")
    print(
        development_sample["sentiment"]
        .value_counts(normalize=True)
        .sort_index()
    )


if __name__ == "__main__":
    main()