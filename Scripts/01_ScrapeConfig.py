import requests
import json
import os


url = "https://itch.io/games"
response = requests.get(url)
filters = []

start = 0
while True:
    start = response.text.find('<ul>', start)
    if start == -1:
        break

    end = response.text.find('</ul>', start)
    ul_section = response.text[start:end]

    for line in ul_section.split('<li>'):
        if 'href="' in line:
            href_start = line.find('href="') + 6
            href_end = line.find('"', href_start)
            href = line[href_start:href_end]

            if 'tag' in href or 'genre' in href:
                continue

            href = href.replace('/games/', '', 1)
            label_start = line.find('>') + 1
            label_end = line.find('</a>')
            raw_label = line[label_start:label_end].strip()
            cleaned_label = raw_label
            if '<span' in cleaned_label:
                span_start = cleaned_label.find('>') + 1
                cleaned_label = cleaned_label[span_start:].strip()
            cleaned_label = cleaned_label.replace(' ', '_').replace('"', '').replace('>', '').replace('<', '').strip()
            filters.append({'label': cleaned_label, 'href': href})
    start = end

start = response.text.find('<ul class="sorts">')
end = response.text.find('</ul>', start)
sort_section = response.text[start:end]

sort_rules = []


for line in sort_section.split('<li>'):
    if 'href="' in line:
        label_start = line.find('>') + 1
        label_end = line.find('</a>')
        label = line[label_start:label_end].strip()

        href_start = line.find('href="') + 6
        href_end = line.find('"', href_start)
        href = line[href_start:href_end]
        href = href.lstrip('/games/')

        sort_rules.append({'label': label, 'href': href})

def extract_tags_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    tags = []

    start = 0
    while True:
        start = html_content.find('data-value="', start)
        if start == -1:
            break

        start += len('data-value="')
        end = html_content.find('"', start)
        tag_value = html_content[start:end]
        label = f"/span{tag_value}"
        href = f"tag-{tag_value.lower().replace(' ', '-')}"
        tags.append({
            "label": label,
            "href": href
        })

        start = end

    return tags


os.makedirs(os.path.join('..', 'Data', 'Config'), exist_ok=True)


filter_output_file = os.path.join('..', 'Data', 'Config', 'FilterOptions.json')
sort_output_file = os.path.join('..', 'Data', 'Config', 'SortingOptions.json')
tags_output_file = os.path.join('..', 'Data', 'Config', 'TagsOptions.json')

with open(filter_output_file, 'w', encoding='utf-8') as file:
    json.dump(filters, file, ensure_ascii=False, indent=4)

with open(sort_output_file, 'w', encoding='utf-8') as file:
    json.dump(sort_rules, file, indent=4)

tags = extract_tags_from_file(os.path.join('source', 'TagsHtmlBody.txt'))
with open(tags_output_file, 'w', encoding='utf-8') as file:
    json.dump(tags, file, indent=4)

print(f"Filter options saved to {filter_output_file}")
print(f"Sorting rules saved to {sort_output_file}")
print(f"Tags saved to {tags_output_file}")
