
import requests

text_input = input("Enter text to extract keywords: ")

response = requests.post("http://127.0.0.1:5000/api/v1/keywords", json={
    "text": text_input
})

print("Response from API:")
print(response.json())