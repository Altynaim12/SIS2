Flip.kz Mini Data Pipeline
Project Overview:

A lightweight yet complete mini-ETL pipeline designed to extract, clean, and load product data from the dynamic e-commerce website Flip.kz.
The workflow is fully automated with Apache Airflow, demonstrating a complete “from website to database” process.

Key Features

Dynamic Scraping:
Extracts product data from a JavaScript-rendered Flip.kz catalog using Selenium WebDriver.

Data Quality:
Cleans and validates raw scraped data, removes duplicates, handles missing values, and normalizes text and numeric fields.

SQLite Storage:
Stores the processed dataset in a SQLite database (output.db) with a clear, simple schema.

Automation:
Entire pipeline is orchestrated through an Airflow DAG, scheduled to run once per day with built-in logging and retries.

Fallback Mode:
If Flip.kz blocks headless scrapers, the pipeline automatically generates a mock dataset (120+ records) to ensure successful downstream processing.

1. Website Description

Chosen Website:
📌 Flip.kz Books Catalog — https://flip.kz

Flip.kz dynamically renders product listings via JavaScript, requiring a browser automation tool for reliable extraction.
The scraping module (src/scraper.py) uses:

Selenium WebDriver

Automated scrolling to load dynamic content

Robust element selection to capture:

Field	Description
title	Book name
price	Book price (numeric)
url	Direct link to product

If JavaScript blocks or content fails to load, the scraper switches to fallback mode and generates a consistent dataset so the pipeline remains stable.

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

4. How to Run Airflow

Start Services:
Launch the Airflow environment (if using Docker Compose):

docker compose up -d

If you are running Airflow locally (without Docker), start the database:

airflow db init

Access UI:
Open the Airflow web interface:

http://localhost:8080

Trigger DAG:
Locate the flip_books_pipeline DAG, ensure it is ON, and trigger a run.

The pipeline executes tasks sequentially:

Scraping → Cleaning → Loading → SQLite Storage

Airflow will show logs for each step, including browser launch (Selenium), preprocessing, and database insertion.

3. Database Schema

Data is stored in `data/output.db` in a simple schema.

| Table Name | Purpose                     | Key Fields                 | Relationship |
|-----------|-----------------------------|----------------------------|-------------|
| products  | Book catalog from Flip.kz   | id (PK), title, price      | –           |

4. Expected Output

Upon successful completion, the following artifacts and logs will be generated:

Database:
The file data/output.db will be created or updated.
It contains the table products with cleaned and structured Flip.kz book data.

Data Volume:
The database will contain at least 100 records (fallback mode guarantees enough rows even if the website blocks scraping).

Logs:
The Airflow loader task will confirm successful data insertion into SQLite.
The scraper and cleaner tasks will also log:

number of raw items scraped

number of cleaned entries

removed duplicates

final inserted row count
