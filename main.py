import matplotlib.pyplot as plt
import requests
import json
from collections import Counter
from fuzzywuzzy import fuzz

# Fetch data from the Stack Exchange API
response = requests.get("https://api.stackexchange.com/2.3/tags?page=1&pagesize=100&order=desc&sort=popular&site=stackoverflow")
data = response.json()

# Initialize a list to store tags
tag_list = []
for item in data['items']:
    tag_list.append(item['name'])

# Fetch additional pages of tag data
count = 2
while count < 26:
    if (data['has_more'] == True) and (data['quota_remaining'] > 10):
        response = requests.get(f"https://api.stackexchange.com/2.3/tags?page={count}&pagesize=100&order=desc&sort=popular&site=stackoverflow")
        data = response.json()  # Update data with new response
        for items in data['items']:
            tag_list.append(items['name'])
    else:
        print("There are no more pages.")
    count += 1

# Function to check if two tags are similar
def are_tags_similar(tag1, tag2, threshold=80):
    similarity_score = fuzz.partial_ratio(tag1, tag2)
    return similarity_score >= threshold

# Create a dictionary to store similar tags
similar_tags_dict = {}

# Group similar tags together
for tag in tag_list:
    grouped = False
    for similar_tag, similar_group in similar_tags_dict.items():
        if are_tags_similar(tag, similar_tag):
            similar_group.append(tag)
            grouped = True
            break
    if not grouped:
        similar_tags_dict[tag] = [tag]

# Count occurrences of similar tag groups
similar_tags_counts = {tag: len(similar_group) for tag, similar_group in similar_tags_dict.items()}

# Get the top ten most common similar tags
top_ten_similar = Counter(similar_tags_counts).most_common(10)
top_ten_similar_dict = dict(top_ten_similar)

# Create a bar chart using matplotlib
plt.bar(top_ten_similar_dict.keys(), top_ten_similar_dict.values())
plt.xlabel('Tag')
plt.ylabel('Count')
plt.title('Top Ten Similar Occurrences')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Show the bar chart
plt.show()