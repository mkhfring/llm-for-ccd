import os
import re
import json
import pathlib


current_location = pathlib.Path(__file__).parent.resolve()


def read_data(data_file):
    with open(data_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            
    return data


def read_lines(file_path):
    unprocessed_results = []
    with open(file_path, 'r') as f:
        for line in f:
            if '**' in line:
                block_begin = ''
            
            block_begin = block_begin + line.strip()
            
            if '++' in line:
                unprocessed_results.append(block_begin) 
          
    return unprocessed_results
            

def extract_results(pure_results):
    result = {}
    for data in pure_results:
        try:
            data_id = int(re.search(r"Data Id (\d+):", data).group(1))
        except:
            assert 1 == 1
            
        try:
            data_value = int(re.search(r"final result\s*.*?\s*:\s*(\d+)", data, re.IGNORECASE).group(1))
        except:
            data_value = data
            
        result[data_id] = data_value
        
    return result
        
            
java_results = read_lines(os.path.join(current_location, 'results_for_java.txt'))
java_ruby_results = read_lines(os.path.join(current_location, 'results_for_java_ruby.txt'))

java_processed_results = extract_results(java_results)
java_ruby_processed_results = extract_results(java_ruby_results)

for key, value in java_processed_results.items():
    if value not in [0, 1]:
        new_value = re.search(r"(0)+", value, re.IGNORECASE)
        if new_value:
            java_processed_results[key] = int(new_value.group(1))
            assert 1 == 1
        
 
original_java_data = read_data(os.path.join(current_location, 'java_test_clone.jsonl'))
original_ruby_java_data = read_data(os.path.join(current_location, 'ruby_java_test_clone.jsonl'))
assert 1 == 1