import base64
import requests
import os
from dotenv import load_dotenv
import json


# Load the environment variables from the .env file
load_dotenv()

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Ensure API key is available
if not api_key:
    raise ValueError("No API key found. Please set your OPENAI_API_KEY in the .env file.")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "images/Hebron_1960.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
   
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Read through this document, completely ignore annotations, new line characters (\n), and vertical lines. Put the output in the format of title, body, and caption. Only respond with a JSON format. Keep everything on 1 line, do not include spaces."
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 1000
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    response_json = response.json()
    # Extract the 'content' section of the message
    content = response_json['choices'][0]['message']['content']
    
    json_data = json.loads(content) # Convert to JSON

    print("title:", json_data["title"])
    print("body:", json_data["body"])
    print("caption:", json_data["caption"])
    


else:
    print("Failed to get a successful response from the API")