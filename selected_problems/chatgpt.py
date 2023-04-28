import os
import json
import pathlib

import requests

from analyse import Analyser
from examples import example1, example2, example3


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
    def __init__(self, data_file, temperature=0.3, model='gpt-3.5-turbo',
                 nl_instruction = 'do code 1 and code 2 solve identical problems with the same inputs and outputs ? answer with yes or no and no explanation.') -> None:
        self.model = model
        self.temperature = temperature
        self.data_file = data_file
        self.output_file = None
        self.data = self._read_data(data_file)
        self.prompts = [self._make_probmpt(d['id'], d['code1'], d['code2'], nl_instruction) for d in self.data]
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

    def _make_probmpt(self, id, code1, code2, nl_instruction):
        prompt = f"""
        code1:
        {code1}
        code2:
        {code2}
        {nl_instruction}
        """
        return (id, prompt)
    
    def run_processing(self, requested_samples_file, output_file):
        self.output_file = output_file
        self.gpt.process_prompts(self.prompts, requested_samples_file, output_file)
        return self


class CloneDetectionWithExamle(CodeCloneDetection):
    def __init__(self, data_file, temperature=0.3, model='gpt-3.5-turbo', nl_instruction='do code 1 and code 2 solve identical problems with the same inputs and outputs ? answer with yes or no and no explanation.') -> None:
        super().__init__(data_file, temperature, model, nl_instruction)
    
    def _make_probmpt(self, id, code1, code2, nl_instruction):
        prompt = f"""
        code example1:{example1} 
        and 
        code example2:{example2}
        solve identical problems. They both take a date as input and output which day of the week the input date is. So, they are code clones.
        code1:
        {code1}
        code2:
        {code2}
        {nl_instruction}
        """
        return (id, prompt)

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
        os.path.join(current_location, 'results', 'results_for_java_ruby2.txt')
    )
    cross_lingual_analyser.compute_metrics('Metrics for ruby java temperature 03', save_to_file=True)
    
    ccd03_prompt1 = CodeCloneDetection(
        os.path.join(current_location, 'java_test_clone_2.jsonl'),
        temperature=0.3,
        nl_instruction='Are code1 and code2 code clones?answer with yes or no and no explanation.'
    )
    ccd03_prompt1.run_processing(
        os.path.join(current_location, 'requested_ids_0.3_prompt1.txt'),
        os.path.join(current_location, 'results', 'results_for_java_prompt1.txt')
    )
    analyser_prompt1 = Analyser(
        ccd03_prompt1.data_file,
        ccd03_prompt1.output_file
    )
    analyser_prompt1.compute_metrics(
        'Metrics for Java temperature 0.3 prompt1',
        save_to_file=True
    )
    
    #Prompt1_Ruby_java
    ccd03_prompt1_ruby_java = CodeCloneDetection(
        os.path.join(current_location, 'ruby_java_test_clone2.jsonl'),
        temperature=0.3,
        nl_instruction='Are code1 and code2 code clones?answer with yes or no and no explanation.'
    )
    ccd03_prompt1_ruby_java.run_processing(
        os.path.join(current_location, 'results', 'requested_ids_0.3_prompt1_ruby_java.txt'),
        os.path.join(current_location, 'results', 'results_for_java_ruby_prompt1.txt')
    )
    analyser_prompt1_ruby_java = Analyser(
        ccd03_prompt1_ruby_java.data_file,
        ccd03_prompt1_ruby_java.output_file
    )
    analyser_prompt1_ruby_java.compute_metrics(
        'Metrics for Java Ruby with temperature 0.3 prompt1',
        save_to_file=True
    )
    assert 1 == 1
    
    ccd01_prompt2 = CodeCloneDetection(
        os.path.join(current_location, 'java_test_clone_2.jsonl'),
        temperature=0.3,
        nl_instruction='do code 1 and code 2 solve identical problems? answer with yes or no and no explanation.'
    )
    ccd01_prompt2.run_processing(
        os.path.join(current_location, 'results', 'requested_ids_0.3_prompt2.txt'), 
        os.path.join(current_location, 'results', 'results_java_03_prompt2.txt')
    )
    analyser_prompt2 = Analyser(
        ccd01_prompt2.data_file,
        ccd01_prompt2.output_file
    )
    analyser_prompt2.compute_metrics('Metrics for java temperature 0.3 prompt2', save_to_file=True)
    
    # Ruby-Java
    ccd01_prompt2_ruby_java = CodeCloneDetection(
        os.path.join(current_location, 'ruby_java_test_clone2.jsonl'),
        temperature=0.3,
        nl_instruction='do code 1 and code 2 solve identical problems? answer with yes or no and no explanation.'
    )
    ccd01_prompt2_ruby_java.run_processing(
        os.path.join(current_location, 'results', 'requested_ids_0.3_prompt2_ruby_java.txt'), 
        os.path.join(current_location, 'results', 'results_java_03_prompt2_ruby_java.txt')
    )
    analyser_prompt2_ruby_java = Analyser(
        ccd01_prompt2_ruby_java.data_file,
        ccd01_prompt2_ruby_java.output_file
    )
    analyser_prompt2_ruby_java.compute_metrics('Metrics for ruby-java temperature 0.3 prompt2', save_to_file=True)
    
    ##With one random Example
    cc03_java_with_example = CloneDetectionWithExamle(
        os.path.join(current_location, 'java_test_clone_small.jsonl'),
        temperature=0.3,
    )
    cc03_java_with_example.run_processing(
        os.path.join(current_location, 'results', 'requested_ids_0.3_java_with_example.txt'), 
        os.path.join(current_location, 'results', 'results_java_03_with_example.txt')
    )
    analyser_java_with_example = Analyser(
        cc03_java_with_example.data_file,
        cc03_java_with_example.output_file
    )
    analyser_java_with_example.compute_metrics('Metrics for Java with example temperature 0.3', save_to_file=True)

    #using description
    # ccd03_prompt_description_java = CodeCloneDetection(
    #     os.path.join(current_location, 'java_test_clone_2.jsonl'),
    #     temperature=0.3,
    #     nl_instruction='Do code1 and code2 have the same description? answer with yes or no and no explanation.'
    # )
    # ccd03_prompt_description_java.run_processing(
    #     os.path.join(current_location, 'results', 'requested_ids_0.3_prompt_description_java.txt'),
    #     os.path.join(current_location, 'results', 'results_for_java_prompt_Description.txt')
    # )
    # analyser_prompt_description_java = Analyser(
    #     ccd03_prompt_description_java.data_file,
    #     ccd03_prompt_description_java.output_file
    # )
    # analyser_prompt_description_java.compute_metrics(
    #     'Metrics for Java with temperature 0.3 description prompt',
    #     save_to_file=True
    # )
    
    #Java Ruby Description
    # ccd03_prompt_description_ruby_java = CodeCloneDetection(
    #     os.path.join(current_location, 'ruby_java_test_clone2.jsonl'),
    #     temperature=0.3,
    #     nl_instruction='Do code1 and code2 have the same description? answer with yes or no and no explanation.'
    # )
    # ccd03_prompt_description_ruby_java.run_processing(
    #     os.path.join(current_location, 'results', 'requested_ids_0.3_prompt_description_ruby_java.txt'),
    #     os.path.join(current_location, 'results', 'results_for_ruby_java_prompt_Description.txt')
    # )
    # analyser_prompt_description_ruby_java = Analyser(
    #     ccd03_prompt_description_ruby_java.data_file,
    #     ccd03_prompt_description_ruby_java.output_file
    # )
    # analyser_prompt_description_ruby_java.compute_metrics(
    #     'Metrics for Ruby and Java with temperature 0.3 description prompt',
    #     save_to_file=True
    # )

if __name__ == "__main__":
    main()

