import requests
import csv
import os
import shutil
import time
import random
from bs4 import BeautifulSoup
import re

def extract_tag_from_url(url):
    match = re.search(r'tag-([^&]*)', url)
    return match.group(1).replace("-", " ") if match else "N/A"

def clean_tag(tag):
    return tag.split("?")[0]

def copy_api_file(source=os.path.join('..', 'Data', 'apis.csv'), destination="TEMP/api.csv"):
    if not os.path.exists(destination):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy(source, destination)
        print(f"Copied {source} to {destination}")
    else:
        print(f"Using existing API file: {destination}")

def load_api_list(file_path="TEMP/api.csv"):
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def update_api_list(api_list, file_path="TEMP/api.csv"):
    fieldnames = ["ID", "API"]
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(api_list)

def fetch_itchio_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def parse_game_data(html_content, tag):
    tag = clean_tag(tag)  
    soup = BeautifulSoup(html_content, "html.parser")
    games = []
    
    for game_div in soup.find_all("div", class_="game_cell"):
        game_id = game_div.get("data-game_id", "N/A")
        title_tag = game_div.find("a", class_="title")
        title = title_tag.text.strip() if title_tag else "N/A"
        href = title_tag.get("href", "N/A") if title_tag else "N/A"

        price_tag = game_div.find("div", class_="price_tag")
        price = price_tag.text.strip() if price_tag and price_tag.text.strip() not in ["", "0"] else "Free"

        author_tag = game_div.find("div", class_="game_author")
        author = author_tag.text.strip() if author_tag else "N/A"

        genre_tag = game_div.find("div", class_="game_genre")
        genre = genre_tag.text.strip() if genre_tag and genre_tag.text.strip() else "None"

        platform_tags = game_div.find_all("span", class_="icon")
        platforms = ", ".join(tag.get("title", "").replace("Download for ", "").strip() for tag in platform_tags if "title" in tag.attrs) if platform_tags else "N/A"

        games.append({
            "game_id": game_id,
            "title": title,
            "price": price,
            "author": author,
            "genre": genre,
            "platforms": platforms,
            "url": href,
            "tags": tag  
        })
    
    return games

def save_to_csv(data, filename=os.path.join('..', 'Data', 'ScrapedInformation.csv'), start_id=1):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    fieldnames = ["scraped_id", "game_id", "title", "price", "author", "genre", "platforms", "url", "tags"]
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
        if os.path.getsize(filename) == 0:
            writer.writeheader()

        for i, game in enumerate(data, start=start_id):
            game["scraped_id"] = i
            writer.writerow(game)

def get_last_scraped_id(filename=os.path.join('..', 'Data', 'ScrapedInformation.csv')):
    if not os.path.exists(filename):
        return 0

    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        rows = list(reader)
        if rows:
            return int(rows[-1]["scraped_id"])
        return 0

def remove_apis_with_prefix(api_list, prefix):
    return [api for api in api_list if not api["API"].startswith(prefix)]

def main():
    copy_api_file()
    temp_file = "TEMP/api.csv"
    api_list = load_api_list(temp_file)
    last_scraped_id = get_last_scraped_id()

    while api_list:
        current_api = api_list.pop(0)
        url = current_api["API"]
        tag = extract_tag_from_url(url)
        print(f"Fetching data from {url} (Tag: {tag})")

        data = fetch_itchio_data(url)

        # If first attempt fails, try replacing "tag" with "genre"
        if data is None:
            new_url = url.replace("tag-", "genre-")
            print(f"First attempt failed. Retrying with: {new_url}")
            data = fetch_itchio_data(new_url)
            if data is not None:
                tag = tag.replace("tag-", "genre-") 
            else:
                print(f"Both attempts failed. Skipping API: {url}")
                continue  

        if data.get("num_items", 0) == 0:
            prefix = url.split("?page=")[0]
            api_list = remove_apis_with_prefix(api_list, prefix)
            print(f"No items found. Removed all APIs starting with {prefix}")
        else:
            parsed_data = parse_game_data(data.get("content", ""), tag)
            save_to_csv(parsed_data, start_id=last_scraped_id + 1)
            last_scraped_id += len(parsed_data)
            print(f"Data from {url} saved successfully!")

        update_api_list(api_list, temp_file)
        time.sleep(random.uniform(4, 5))
    
    print("Scraping complete.")

if __name__ == "__main__":
    main()
