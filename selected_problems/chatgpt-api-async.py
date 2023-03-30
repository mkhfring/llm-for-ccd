import asyncio
import httpx
import json

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
            "temperature": 0.7
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            return response.json()

    async def process_prompts(self, prompts):
        tasks = [self._send_request(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks)
        self.results.extend(results)

    def display_results(self):
        for idx, result in enumerate(self.results):
            print(f"Result {idx + 1}: {result['choices'][0]['message']['content'].strip()}")

async def main():
    chat_gpt = ChatGPTAsync()
    prompts = ["Hello Chatgpt", "How are you?", "count to 3"]
    await chat_gpt.process_prompts(prompts)
    chat_gpt.display_results()

if __name__ == "__main__":
    asyncio.run(main())
