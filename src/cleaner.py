import os
import pandas as pd


def clean_data():
    """
    Clean raw_flip.csv and save to clean_flip.csv
    """
    raw_path = "data/raw_flip.csv"
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"{raw_path} not found. Run scraper first.")

    df = pd.read_csv(raw_path)

    # Drop duplicates
    df = df.drop_duplicates()

    # Normalize price → numeric
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace("\u00a0", "", regex=False)
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Drop rows without price
    df = df.dropna(subset=["price"])

    # Normalize title
    df["title"] = df["title"].astype(str).str.strip()

    # Drop rows with very short titles (noise)
    df = df[df["title"].str.len() > 2]

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/clean_flip.csv", index=False)
    print(f"Cleaned dataset saved to data/clean_flip.csv with {len(df)} rows")
    return df


if __name__ == "__main__":
    clean_data()
