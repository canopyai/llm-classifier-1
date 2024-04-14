def convert_to_string(messages):
    # Initialize an empty list to hold formatted messages
    formatted_messages = []
    
    # Loop through each message in the list
    for message in messages:
        # Format each message as "role: content"
        formatted_message = f"{message['role']}: {message['content']}"
        # Append the formatted message to the list
        formatted_messages.append(formatted_message)
    
    # Join all formatted messages into a single string with new lines between them
    result_string = "\n".join(formatted_messages)
    
    return result_string