import matplotlib.pyplot as plt
import requests
import json

response = requests.get("https://api.stackexchange.com/2.3/tags?page=1&pagesize=100&order=desc&sort=popular&site=stackoverflow")
data = response.json()
tag_list = []
for item in data['items']:
    tag_list.append(item['name'])

status = True
count = 2
while count < 26:
    if (data['has_more'] == True) and (data['quota_remaining'] > 10):
        response = requests.get(f"https://api.stackexchange.com/2.3/tags?page={count}&pagesize=100&order=desc&sort=popular&site=stackoverflow")
        data = response.json()  # Update data with new response
        for items in data['items']:
            tag_list.append(items['name'])
    else:
        print("There are no more pages.")
        status = False
    count += 1
print(tag_list)
