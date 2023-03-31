import os
import json
import pathlib

import requests


current_location = pathlib.Path(__file__).parent.resolve()



def get_requested_ids(file_name):
    requested_ids = []
    if not os.path.exists(file_name):
        return []
    
    with open(file_name, 'r') as file:
        for line in file:
            requested_ids.append(int(line.strip()))
        
    return requested_ids

def read_data(data_file):
    with open(data_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            
    return data


def make_probmpt(id, code1, code2):
    prompt = f"""
    code1:
    {code1}
    What problem does code1 solves. Name it p1. Then, generate an input and an output for code 1. Now, take code2

    code2:
    {code2}
    
    if code2 dosn't solve p1 then return final result is: 0 and don't continue. if code2 solves p1 then check if outputs are identical for the same input, return 1; otherwise, return 0". Conclude the result with the "final result is:" so that I can find the result easily.
    """
    return (id, prompt)


class ChatGPTRequest:
    def __init__(self):
        self.results = []
        self.api_key = self._read_api_key()

    def _read_api_key(self):
        with open("/Users/mohamadkhajezade/workspace/openai.txt", "r") as file:
            return file.readline().strip()

    def _send_request(self, prompt_id, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f"{prompt}"}],
            "temperature": 0.3
        }
        response = requests.post(url, headers=headers, json=data)
        print(f"The request status for prompt id {prompt_id} is {response.status_code}\n")
        return response.json()

    def process_prompts(self, prompts):
        requested_ids = get_requested_ids(os.path.join(current_location, 'last_id.txt'))
        for prompt in prompts:
            sample_id = prompt[0]
            if sample_id in requested_ids:
                continue
            
            with open(os.path.join(current_location, 'last_id.txt'), 'a') as file:
                file.write(f"{sample_id}\n")
                
            result = self._send_request(prompt[0], prompt[1])
            if not 'choices' in result:
                continue
            
            with open(os.path.join(current_location, 'results_for_java.txt'), 'a') as file:
                file.write(f"***Data Id {sample_id}: {result['choices'][0]['message']['content'].strip()}+++\n \n")

def main():
    chat_gpt = ChatGPTRequest()
    data = read_data(os.path.join(current_location, 'java_test_clone.jsonl'))
    prompts = [make_probmpt(d['id'], d['code1'], d['code2']) for d in data]
    
    chat_gpt.process_prompts(prompts)

if __name__ == "__main__":
    main()

