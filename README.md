# Flip.kz Data Pipeline

## Project Overview
A lightweight yet complete mini-ETL pipeline designed to extract, clean, and load product data from the dynamic e-commerce website **Flip.kz**.  
The workflow is fully automated using **Apache Airflow**, demonstrating a complete **“from website to database”** process.

---

## Key Features

- **Dynamic Scraping** — Extracts product data from a JavaScript-rendered Flip.kz catalog using **Selenium WebDriver**.
- **Data Quality** — Cleans raw scraped data, removes duplicates, handles missing values, and normalizes text and numeric fields.
- **SQLite Storage** — Stores processed data in a SQLite database (`output.db`) with a simple and clear schema.
- **Automation** — Entire pipeline is orchestrated via an **Airflow DAG**, running once per day with built-in logging and retries.
- **Fallback Mode** — If Flip.kz blocks automated scraping, the scraper switches to fallback mode and generates a mock dataset (120+ rows) to guarantee ETL stability.

---

# 1. Website Description

**Chosen Website:** Flip.kz Books Catalog  
**URL:** https://flip.kz  

Flip.kz renders product listings dynamically using JavaScript, requiring a browser automation tool for extraction.

The scraping module (`src/scraper.py`) uses:

- Selenium WebDriver  
- Automated scrolling to load dynamic content  
- Stable HTML element selection  

### Extracted Fields

| Field | Description |
|-------|-------------|
| **title** | Book name |
| **price** | Numeric book price |
| **url** | Direct link to the product |

If JavaScript blocks loading, the scraper generates a fallback dataset to ensure the pipeline remains stable.

---

# 2. Execution and Setup

## Project Structure

flip_books_pipeline/
│
├── README.md
├── requirements.txt
├── airflow_dag.py
│
├── src/
│ ├── scraper.py
│ ├── cleaner.py
│ └── loader.py
│
├── data/
│ ├── raw_flip.csv
│ ├── clean_flip.csv
│ └── output.db
│
└── create_table.sql

---

## How to Run Airflow (Local Environment)

### 1. Install Dependencies
```bash
pip install -r requirements.txt

2. Initialize Airflow
airflow db init

3. Start Airflow Services (Two Terminals)

Terminal 1 — Scheduler

airflow scheduler


Terminal 2 — Webserver

airflow webserver --port 8080

4. Trigger the Pipeline

Open Airflow UI:
http://localhost:8080

Locate the DAG: flip_books_pipeline
Turn it ON → Click Trigger DAG

Pipeline flow:

Scraping → Cleaning → Loading → SQLite Storage

---
# 3. Database Schema

Data is stored in data/output.db using the following schema:

| Table Name   | Purpose              | Key Fields                         | Relationship |
| ------------ | -------------------- | ---------------------------------- | ------------ |
| **products** | Flip.kz book catalog | `id` (PK), `title`, `price`, `url` | —            |


---
#4. Expected Output

1. Raw Dataset

data/raw_flip.csv — raw scraped data or fallback dataset (120+ rows)

2. Clean Dataset

data/clean_flip.csv — cleaned, deduplicated data with normalized types

3. SQLite Database

data/output.db — containing table products with fields:

id

title

price

url

4. Airflow Logs

The following information will appear in Airflow logs:

number of scraped items

number of cleaned entries

duplicates removed

final record count inserted into SQLite
