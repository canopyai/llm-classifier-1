import requests
import time

def post_messages(messages):
    url = "http://35.204.35.46:8080"  # Replace with the appropriate URL

    try:
        response = requests.post(url, json=messages)
        response.raise_for_status()
        print("Messages posted successfully!")
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error posting messages: {e}")

messages = [
    {
        "role": "user",
        "content": "Hello, how are you?"
    },
    {
        "role": "assistant",
        "content": "I'm doing well, thank you!"
    }
]
startTime = time.time()
post_messages(messages)
endTime = time.time()
print(f"Time taken to post messages: {endTime - startTime} seconds")