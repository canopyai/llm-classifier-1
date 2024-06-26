from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import time
import numpy as np
import torch
import torch.nn.functional as F
from utils.get_input_ids import get_input_ids
from utils.normalize_probs_and_map import normalize_probs_and_map
from utils.convert_to_string import convert_to_string

temperature = 1  # For creativity. 1.0 is the default. Lower for more deterministic.
max_length = 50  # Maximum number of tokens to generate.
num_generated_tokens = 1  # Parameter to control the number of tokens to generate
temperature = 1  

app = Flask(__name__)
CORS(app)


model_id = "google/gemma-2b"

is_cuda_available = torch.cuda.is_available()
device = 'cuda' if is_cuda_available else 'cpu'

print("Using device:", device)


tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

model = model.to(device)

emotion_list = ["Happy", "Sad", "Neutral", "Angry", "Disgust", "Excitement", "Fear", "Concern", "Interest", "Surprise", "Curiosity"]
encoded_list = [tokenizer(i)['input_ids'][1] for i in emotion_list]

@app.route('/ping', methods=['GET'])
def pong():
    return 'pong'

@app.route('/', methods=['POST'])
def classify_conversation():
    time0 = time.time()
    data = request.get_json()

    time1 = time.time()
    utext = convert_to_string(data)
    input_ids = get_input_ids(utext, tokenizer, emotion_list)
    new_input_ids = input_ids.to(device).clone()
    time2 = time.time()
    with torch.no_grad():
        for _ in range(num_generated_tokens):
            outputs_l = model(new_input_ids)
            logits = outputs_l.logits
            # Scale logits by temperature
            scaled_logits = logits / temperature
            selected_token_ids = encoded_list
            selected_logits = scaled_logits[:, :, selected_token_ids]
            probabilities = F.softmax(scaled_logits, dim=-1)
            next_token_logits = probabilities[:, -1, :]
            most_probable_token_id = torch.argmax(next_token_logits, dim=-1).item()
            print("most_probable_token_id", most_probable_token_id, tokenizer.decode(most_probable_token_id))
            selected_probabilities = probabilities[:, :, selected_token_ids]
            exp_probabilities = selected_probabilities[:, -1, :]
            next_token_logits = probabilities[:, -1, :]
            # Select the most probable next token ID
            next_token_id = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)
            # Append the generated token ID to the input for the next iteration
            new_input_ids = torch.cat((new_input_ids, next_token_id), dim=1)
    time3 = time.time()
    emotion_prob_map = normalize_probs_and_map(exp_probabilities, emotion_list)
    time4 = time.time()
    print(f'times 1{time1 - time0} 2{time2 - time1} 3{time3 - time2} 4{time4 - time3}')
    return emotion_prob_map


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')