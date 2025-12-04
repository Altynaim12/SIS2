import os
import sqlite3
import pandas as pd


def load_to_sqlite():
    """
    Load clean_flip.csv into SQLite database data/output.db, table products
    """
    clean_path = "data/clean_flip.csv"
    if not os.path.exists(clean_path):
        raise FileNotFoundError(f"{clean_path} not found. Run cleaner first.")

    df = pd.read_csv(clean_path)

    os.makedirs("data", exist_ok=True)
    db_path = "data/output.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            url TEXT
        )
        """
    )

    df.to_sql("products", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    print(f"Loaded {len(df)} rows into {db_path} (table: products)")
    return True


if __name__ == "__main__":
    load_to_sqlite()
