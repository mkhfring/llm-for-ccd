import os
import re
import json
import pathlib

from sklearn.metrics import precision_score, recall_score, f1_score


current_location = pathlib.Path(__file__).parent.resolve()


def get_labels(predictions, ground_truth):
    ground_truth_labels = []
    predictions_labels = []
    for element in ground_truth:
        key = list(element.keys())[0]
        assert 1 == 1
        if key in predictions:
            ground_truth_labels.append(element[key])
            predictions_labels.append(predictions[key])
        
        else:
            assert 1==1
        
    return ground_truth_labels, predictions_labels


def get_ground_trouth_lables(original_data):
    samples_label = [{sample['id']: sample['label']} for sample in original_data]
    return samples_label


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
            
        else:
            java_processed_results[key] = -1
            
            
for key, value in java_ruby_processed_results.items():
    if value not in [0, 1]:
        java_ruby_processed_results[key] = -1
        
 
original_java_data = read_data(os.path.join(current_location, 'java_test_clone.jsonl'))
original_ruby_java_data = read_data(os.path.join(current_location, 'ruby_java_test_clone.jsonl'))
java_ground_truth = get_ground_trouth_lables(original_java_data)
ruby_java_ground_truth = get_ground_trouth_lables(original_ruby_java_data)
java_prediction_ground_truth = get_labels(java_processed_results, java_ground_truth)
java_ruby_prediction_ground_truth = get_labels(java_ruby_processed_results, ruby_java_ground_truth)
assert 1 == 1
precision_java = precision_score(java_prediction_ground_truth[0], java_prediction_ground_truth[1], average='macro')
recall_java = recall_score(java_prediction_ground_truth[0], java_prediction_ground_truth[1], average='macro')
f1_java = f1_score(java_prediction_ground_truth[0], java_prediction_ground_truth[1], average='macro')

precision_java_ruby = precision_score(java_ruby_prediction_ground_truth[0], java_ruby_prediction_ground_truth[1], average='macro')
recall_java_ruby = recall_score(java_ruby_prediction_ground_truth[0], java_ruby_prediction_ground_truth[1], average='macro')
f1_java_ruby = f1_score(java_ruby_prediction_ground_truth[0], java_ruby_prediction_ground_truth[1], average='macro')
assert 1 == 1