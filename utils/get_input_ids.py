import torch
emotion_list = ["Happy", "Sad", "Neutral", "Angry", "Disgust", "Excitement", "Fear", "Concern"]

def get_input_ids(utext, tokenizer):
    input_text = f'''You will classify the next emotion of the assistant from input conversation as one the following: [{", ".join(emotion_list)}]:

    Here are few examples to illustrate only the format:

    Input: I had a great day
    Output: happy

    Input: A bear is coming after me
    Output: fear

    Input: {utext}
    Output: '''
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    token_to_add = torch.tensor([[199]])
    input_ids = torch.cat((input_ids, token_to_add), dim=1) 
    return input_ids
