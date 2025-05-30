# Trustpilot Webscraper

This project scrapes game information from the Itch.io website. It gets game details like titles, prices, platforms, and tags. The project has separate scripts to get config data, build API URLs, scrape the data, and clean it.

---

## Project Structure




## 🚀 Features

- Extracts filter options, sorting rules, and tags from Itch.io for targeted scraping
- Automatically builds API URLs based on filter, sort, and tag combinations
- Scrapes detailed game data including title, price, author, genre, platforms, and tags
- Cleans and normalizes scraped data (e.g., currency conversion, platform splitting)

---

## 🗂️ Project Structure

- `scripts/` — Contains all Python scripts:
  - `01_Scrape_Config.py — Extracts filter and sorting options from saved HTML source files and saves JSON config files`.
  - `02_BuildApis.py — Builds a list of API URLs to scrape`.
  - `03_ScrapeApis.py — fetches data from the API URLs and saves the raw scraped game info`.
  - `04_CleanData.py — cleans and prepares the scraped data for use.`.

- `Source/`:
- `This folder holds the raw HTML file TagsHtmlBody.txt that is used to extract tag information`.


- `data/`:
  - `config/ — JSON config files saved here`.
  - `apis.csv — API URL List`.
  - `ScrapedInformation.csv — Raw scraped data`.
  - `Cleaned_Data.csv — Cleaned data`.

---

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/tatemat99/itchio-webscraper.git
cd itchio-webscraper
```


### 2. Create and Activate a Virtual Environment (Recommended)

Create a Python virtual environment to isolate dependencies:

macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```bash
python -m venv venv
venv\Scripts\activate
```


### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

### 1: Generate filter, sorting, and tags config files

```python 01_ScrapeConfig.py
```
Creates JSON config files (FilterOptions.json, SortingOptions.json, TagsOptions.json) in Data/config/..


### 2: Build the list of API URLs to scrape

```python 02_BuildApis.py
```
Generates apis.csv in Data/ containing all API endpoints based on configs.


### 3: Scrape game data from Itch.io APIs

```python 03_ScrapeApis.py
```
Fetches game data from APIs listed in apis.csv and saves raw data to Data/raw/ScrapedInformation.csv.


### 4: Clean and normalize scraped game data

```python 04_CleanData.py
```
Processes and cleans the raw scraped data, saving the output to Data/cleaned/Cleaned_Data.csv.

---

## 📝 Notes

- Scripts should be run from the /Scripts directory to ensure relative paths work correctly.

- The scraper includes basic error handling, but network issues or changes in Itch.io’s API or HTML may require script updates.

- Install all dependencies using pip install -r requirements.txt before running scripts.

---