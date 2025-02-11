import requests, os, csv, random
from datetime import datetime

def prompt_llm_for_response(model_name, prompt):
    payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}]
        }

    response = requests.post(f"http://localhost:1234/v1/chat/completions", json=payload)

    if response.status_code == 200:
        data = response.json()
        response_text = data.get("choices", [{}])[0].get("message", "Error").get("content", "No response")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return
    return response_text

def prompt_llm_for_structured_response(model_name, json_schema, prompt):
    payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": json_schema
        }

    response = requests.post(f"http://localhost:1234/v1/chat/completions", json=payload)

    if response.status_code == 200:
        data = response.json()
        response_text = data.get("choices", [{}])[0].get("message", "Error").get("content", "No response")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return
    return response_text

def save_text_to_file_with_unique_name(text, file_name, directory_name):
    current_datetime_string = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    dynamic_file_name = f"{file_name}_{current_datetime_string}.txt"
    file_path = os.path.join(directory_name, dynamic_file_name)
    os.makedirs(directory_name, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(text)

def generate_random_debate_topic():
    with open('data/IBMDebatingTopicDataset.csv', newline='') as f:
        reader = csv.reader(f)
        data = [row[0] for row in reader]
    return random.choice(data)

def make_conversation_prompt_from_topic(topic):
    return f"The focus of the conversation is to debate your opinions around the following topic: {topic}"
