Flip.kz Mini Data Pipeline
Project Overview

A lightweight but complete mini-ETL pipeline designed to extract, clean, and load product data from the dynamic e-commerce website Flip.kz.
The workflow is automated using Apache Airflow, demonstrating a full “from website to database” process.

Key Features

Dynamic Scraping
Extracts product data from the JavaScript-rendered Flip.kz catalog using Selenium WebDriver.

Data Quality
Cleans raw scraped data, removes duplicates, handles missing values, and normalizes text and numeric fields.

SQLite Storage
Stores processed data in a SQLite database (output.db) using a simple and clear schema.

Automation
The entire pipeline is orchestrated via an Airflow DAG, scheduled to run once per day with logging and retries.

Fallback Mode
If Flip.kz blocks automated scraping, the pipeline switches to fallback mode and generates a mock dataset (120+ rows) to guarantee ETL stability.

1. Website Description

Chosen Website: Flip.kz Books Catalog — https://flip.kz

Flip.kz renders product listings dynamically using JavaScript, so a browser automation tool is required for extraction.

The scraping module (src/scraper.py) uses:

Selenium WebDriver

Automated scrolling to load dynamic content

Stable HTML element selection

Extracted Fields
Field	Description
title	Book name
price	Numeric book price
url	Direct link to the product

If JavaScript blocks access, the scraper automatically switches to fallback mode and generates a consistent dataset.

2. Execution and Setup
Project Structure
flip_books_pipeline/
│
├── README.md
├── requirements.txt
├── airflow_dag.py
│
├── src/
│   ├── scraper.py
│   ├── cleaner.py
│   └── loader.py
│
├── data/
│   ├── raw_flip.csv
│   ├── clean_flip.csv
│   └── output.db
│
└── create_table.sql

3. How to Run Airflow
Start Services (Docker Compose)
docker compose up -d

If running Airflow locally (without Docker)

Initialize Airflow database:

airflow db init


Start webserver:

airflow webserver -p 8080


Start scheduler:

airflow scheduler

Access the Web Interface

Open:

http://localhost:8080


Locate and enable the DAG:

flip_books_pipeline


Trigger a run.

Pipeline Execution Order
Scraping → Cleaning → Loading → SQLite Storage


Airflow logs will show scraping progress, cleaning operations, and database insertion details.

4. Database Schema

Data is stored in data/output.db.

Table: products
Column	Type	Description
id	INTEGER PRIMARY KEY	Unique identifier
title	TEXT	Book name
price	REAL	Numeric price
url	TEXT	Direct product link
5. Expected Output

After successful execution, the following outputs will be generated:

1. Raw Data

data/raw_flip.csv
Contains scraped data or fallback dataset (120+ rows).

2. Cleaned Data

data/clean_flip.csv
Includes:

normalized types

removed duplicates

missing values handled

3. SQLite Database

data/output.db containing:

products (id, title, price, url)

4. Airflow Logs

Logs from scraper, cleaner and loader tasks will include:

Number of scraped items

Number of cleaned items

Number of duplicates removed

Final inserted row count