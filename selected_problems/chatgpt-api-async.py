import os
import json
import pathlib
import asyncio
import httpx


current_location = pathlib.Path(__file__).parent.resolve()


def read_data(data_file):
    with open(data_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            
    return data

def make_probmpt(code1, code2):
    prompt = f"""
    code1:
    {code1}
    generate an input and an output for code 1. Now, take code2

    code2:
    {code2}
    
    If code1 and code2 solve different problems return 0. If the outputs are identical for the same input, return 1; otherwise, return 0". Conclude the result with the "final result is:" so that I can find the result easily.
    """
    return prompt

class ChatGPTAsync:
    def __init__(self):
        self.results = []
        self.api_key = self._read_api_key()

    def _read_api_key(self):
        with open("/Users/mohamadkhajezade/workspace/openai.txt", "r") as file:
            return file.readline().strip()

    async def _send_request(self, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f"{prompt}"}],
            "temperature": 0.1
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            return response.json()

    async def process_prompts(self, prompts):
        tasks = [self._send_request(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks)
        self.results.extend(results)

    def display_results(self):
        with open(os.path.join(current_location, 'results_for_java.txt'), 'a') as file:
            for idx, result in enumerate(self.results):
                file.write(f"Data Id {idx}: {result['choices'][0]['message']['content'].strip()}\n")
            

async def main():
    chat_gpt = ChatGPTAsync()
    data = read_data(os.path.join(current_location, 'java_test_clone.jsonl'))
    data = data[0:2]
    
    prompts = [make_probmpt(d['code1'], d['code2']) for d in data]
    
    await chat_gpt.process_prompts(prompts)
    chat_gpt.display_results()

if __name__ == "__main__":
    asyncio.run(main())
