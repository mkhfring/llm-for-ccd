import os
import json
import pathlib

import requests

from analyse import Analyser


current_location = pathlib.Path(__file__).parent.resolve()


class ChatGPTRequest:
    def __init__(self, temperature=0.3, model='gpt-3.5-turbo'):
        self.temperature = temperature
        self.model = model
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
            "model": self.model,
            "messages": [{"role": "user", "content": f"{prompt}"}],
            "temperature": self.temperature
        }
        response = requests.post(url, headers=headers, json=data)
        print(f"The request status for prompt id {prompt_id} is {response.status_code}\n")
        return response.json()

    def process_prompts(self, prompts, requested_samples_file, output_file):
        requested_ids = self._get_requested_ids(requested_samples_file)
        for prompt in prompts:
            sample_id = prompt[0]
            if sample_id in requested_ids:
                continue
            
            with open(requested_samples_file, 'a') as file:
                file.write(f"{sample_id}\n")
                
            result = self._send_request(prompt[0], prompt[1])
            if not 'choices' in result:
                continue
            
            with open(output_file, 'a') as file:
                file.write(f"***Data Id {sample_id}: {result['choices'][0]['message']['content'].strip()}+++\n \n")
                
    def _get_requested_ids(self, requested_sample_file):
        requested_ids = []
        if not os.path.exists(requested_sample_file):
            return []
        with open(requested_sample_file, 'r') as file:
            for line in file:
                requested_ids.append(int(line.strip()))
            
        return requested_ids
                
               
class CodeCloneDetection:
    def __init__(self, data_file, temperature=0.3, model='gpt-3.5-turbo' ) -> None:
        self.model = model
        self.temperature = temperature
        self.data_file = data_file
        self.output_file = None
        self.data = self._read_data(data_file)
        self.prompts = [self._make_probmpt(d['id'], d['code1'], d['code2']) for d in self.data]
        self.gpt = ChatGPTRequest(temperature=self.temperature, model=self.model)
    
    def _get_requested_ids(self, file_name):
        requested_ids = []
        if not os.path.exists(file_name):
            return []
        with open(file_name, 'r') as file:
            for line in file:
                requested_ids.append(int(line.strip()))
            
        return requested_ids

    def _read_data(self, data_file):
        with open(data_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                
        return data

    def _make_probmpt(self, id, code1, code2):
        prompt = f"""
        code1:
        {code1}
        code2:
        {code2}
        do code 1 and code 2 solve identical problems with the same inputs and outputs? answer with yes or no and no explanation. 
        """
        return (id, prompt)
    
    def run_processing(self, requested_samples_file, output_file):
        self.output_file = output_file
        self.gpt.process_prompts(self.prompts, requested_samples_file, output_file)
        return self


def main():
    # chat_gpt = ChatGPTRequest()
    # data = read_data(os.path.join(current_location, 'java_test_clone_2.jsonl'))
    
    
    # chat_gpt.process_prompts(prompts)
    ccd01 = CodeCloneDetection(
        os.path.join(current_location, 'java_test_clone_2.jsonl'),
        temperature=0.1
    )
    ccd01.run_processing(
        os.path.join(current_location, 'results', 'requested_ids_0.1.txt'), 
        os.path.join(current_location, 'results', 'results_java_01.txt')
    )
    analyser1 = Analyser(
        ccd01.data_file,
        ccd01.output_file
    )
    analyser1.compute_metrics('Metrics for java temperature 0.1', save_to_file=True)
    analyser2 = Analyser(
        ccd01.data_file,
        os.path.join(current_location, 'results','results_for_java2.txt')
    )
    analyser2.compute_metrics('Metrics for java temperature 0.3', save_to_file=True)
    
    ccd05 = CodeCloneDetection(
        os.path.join(current_location, 'java_test_clone_2.jsonl'),
        temperature=0.5
    )
    ccd05.run_processing(
        os.path.join(current_location, 'results', 'requested_ids_0.5.txt'), 
        os.path.join(current_location, 'results', 'results_java_0.5.txt')
    )
    analyser3 = Analyser(
        ccd05.data_file,
        ccd05.output_file
    )
    analyser3.compute_metrics('Metrics for java temperature 0.5', save_to_file=True)
    cross_lingual_analyser = Analyser(
        os.path.join(current_location, 'ruby_java_test_clone2.jsonl'),
        os.path.join(current_location, 'results_for_java_ruby2.txt')
    )
    cross_lingual_analyser.compute_metrics('Metrics for ruby java temperature 03', save_to_file=True)
    
    assert 1 == 1

if __name__ == "__main__":
    main()

