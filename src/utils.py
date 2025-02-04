import requests

def prompt_llm_for_response(model_name, prompt):
    payload = {
            "model": model_name,
            "prompt": prompt,
        }

    response = requests.post(f"http://localhost:1234/v1/completions", json=payload)

    if response.status_code == 200:
        data = response.json()
        response_text = data.get("choices", [{}])[0].get("text", "No response")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return
    return response_text