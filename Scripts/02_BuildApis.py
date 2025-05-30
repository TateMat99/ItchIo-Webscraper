import csv
import os
import time
import json
from itertools import combinations


sorting_file = os.path.join('..', 'Data', 'Config', 'SortingOptions.json')
filter_file = os.path.join('..', 'Data', 'Config', 'FilterOptions.json')
tags_file = os.path.join('..', 'Data', 'Config', 'TagsOptions.json')
output_file = os.path.join('..', 'Data', 'apis.csv')

# Base URL and max pagination
base_url = "https://itch.io/games"
max_page = 200  #  general Pagination limit from itch.io

#generate and save API URLs
def generate_and_save_api_urls(base_url, sorting_options, filter_options, tag_options, max_page, output_file):
    api_id = 1  

    os.makedirs(os.path.join('..', 'Data'), exist_ok=True)


    with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'API'])
        
        for sort in sorting_options:
            for tag in tag_options:  
                tag_path = tag['href'] if tag else ''

                for page in range(1, max_page + 1):
                    if tag_path:
                        url = f"{base_url}/{sort}/{tag_path}?page={page}&format=json"
                    else:
                        url = f"{base_url}/{sort}?page={page}&format=json"

                    url = url.replace('//', '/').replace('https:/', 'https://')
                    writer.writerow([api_id, url])
                    print(f"Saved API #{api_id}: {url}")
                    api_id += 1


def filter_combinations(options):
    for r in range(len(options) + 1):
        for combo in combinations([item['href'] for item in options], r):
            yield combo

print("Starting API URL generation script...")
print(f"Loading sorting options from: {sorting_file}")
print(f"Loading filter options from: {filter_file}")
print(f"Loading tag options from: {tags_file}")

with open(sorting_file, 'r', encoding='utf-8') as file:
    sorting_options = [item['href'] for item in json.load(file)]

with open(filter_file, 'r', encoding='utf-8') as file:
    filter_options = json.load(file)

with open(tags_file, 'r', encoding='utf-8') as file:
    tag_options = json.load(file)

print(f"Sorting options loaded: {sorting_options}")
print(f"Filter options loaded: {filter_options}")
print(f"Tag options loaded: {tag_options}")
print(f"Generating and saving API URLs to: {output_file}")
generate_and_save_api_urls(base_url, sorting_options, filter_options, tag_options, max_page, output_file)

print("API URL generation and saving completed!")
