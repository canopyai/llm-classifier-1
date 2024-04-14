import requests

def post_messages(messages):
    url = "http://35.204.35.46:8085"  # Replace with the appropriate URL

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

post_messages(messages)