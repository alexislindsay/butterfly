import json

# Load and preview the extracted conversations.json
conversations_json_path = os.path.join(extracted_path, 'conversations.json')

with open(conversations_json_path, 'r', encoding='utf-8') as f:
    conversations_data = json.load(f)

# Preview the structure (first entry or two)
conversations_data[:2]  # just to glimpse how it's structured
