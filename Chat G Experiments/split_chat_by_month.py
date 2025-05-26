import re
from datetime import datetime

# Load data from your chat file
with open(r"C:\Users\alexi\Downloads\Chat G\chat.txt", 'r', encoding='utf-8') as file:
    chat_data = file.read()

# Define a regex pattern to find dates in YYYY-MM-DD format
date_pattern = r"(\d{4}-\d{2})-\d{2}"

# Find all dates in the format YYYY-MM-DD and extract year-month (YYYY-MM)
matches = re.findall(date_pattern, chat_data)

# Split the chat data using the full date pattern
chunks = re.split(r"\d{4}-\d{2}-\d{2}", chat_data)

# Create a dictionary to store chunks by year-month
split_data = {}

# Attach each chunk to its corresponding year-month key
for i in range(len(chunks) - 1):
    year_month = matches[i]
    if year_month not in split_data:
        split_data[year_month] = ""
    split_data[year_month] += chunks[i + 1]

# Write each month's chunk to a separate file
for year_month, content in split_data.items():
    filename = f'chat_{year_month}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"{year_month}\n{content}")

print("Chat history has been successfully split into monthly chunks.")
