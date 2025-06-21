import json
import requests

# Load your JSON file (adjust filename if needed)
with open("portfolio_qa_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# FastAPI endpoint URL
API_URL = "http://localhost:8000/api/v1/add"

# Loop through and send POST requests
for item in data:
    payload = {
        "text": item["text"],
        "metadata": item["metadata"]
    }

    print(f"Uploading: {item['text'][:60]}...")
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("✅ Success:", response.json())
        else:
            print("❌ Failed:", response.status_code, response.text)
    except Exception as e:
        print("❌ Error:", str(e))

    print("----")
