import openai

def read_api_key():
    with open("/Users/mohamadkhajezade/workspace/openai.txt", "r") as file:
        return file.readline().strip()

def send_request(prompt, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=1.0,
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    api_key = read_api_key()
    prompt = "Write a Python function to calculate the factorial of a number."

    response_text = send_request(prompt, api_key)
    print("Generated code:\n", response_text)