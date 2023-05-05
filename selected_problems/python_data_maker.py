import os
import json
import pathlib
import random


current_location = pathlib.Path(__file__).parent.resolve()
python = os.path.join(current_location, 'python_selected')
ruby = os.path.join(current_location, 'ruby_selected')

python_problems = os.listdir(python)
data = []


def count_tokens(text):
    words = text.split()
    return len(words)


#Positive samples: 
id_count = 0
positive_count = 0
negative_count = 0
for p in python_problems: 
    if '.' in p:
        continue
    
    submissions = os.listdir(os.path.join(python, p))
    for i in range(3):
        if positive_count > 500:
            break
        for j in range(i+1, len(submissions)):
            if j - i > 3:
                break;
            if positive_count > 500:
                break
            
            with open(os.path.join(python, p, submissions[i]), 'r') as f:
                code1 = f.read()
                code1_name = f.name
                
            with open(os.path.join(python, p, submissions[j]), 'r') as f:
                code2 = f.read()
                code2_name = f.name
                
            
                
            number_of_tokens = count_tokens(code1) + count_tokens(code2)
            assert 1 == 1
            if number_of_tokens > 3000:
                continue
                
            element = {
                'id': id_count,
                'code1': code1,
                'code2': code2,
                'label': 1,
                'name1': os.path.basename(code1_name), 
                'name2': os.path.basename(code2_name)
            }
            data.append(element)
            positive_count = positive_count + 1
            id_count = id_count + 1
            
#negative samples
python_problems = [p for p in python_problems if '.' not in p]
for i in range(len(python_problems)):
    if negative_count > 500:
        break
    for j in range(i+1, len(python_problems)):
        if negative_count > 500:
            break
    
        if j - i > 2:
            break
        
        problem1 = python_problems[i]
        problem2 = python_problems[j]
        if problem1 == problem2:
            continue
        
        p1_sub = os.listdir(os.path.join(python, problem1))
        p2_sub = os.listdir(os.path.join(python, problem2))
        
        for index in range(3):
            
            with open(os.path.join(python, problem1, p1_sub[index]), 'r') as f:
                code1 = f.read()
                code1_name = f.name
                
            with open(os.path.join(python, problem2, p2_sub[index]), 'r') as f:
                code2 = f.read()
                code2_name = f.name
                
            number_of_tokens = count_tokens(code1) + count_tokens(code2)
            assert 1 == 1
            if number_of_tokens > 3000:
                continue
            element = {
                'id': id_count,
                'code1': code1,
                'code2': code2,
                'label': 0,
                'name1': os.path.basename(code1_name), 
                'name2': os.path.basename(code2_name)
            }
            data.append(element)
            id_count = id_count + 1
            negative_count = negative_count + 1

random.shuffle(data)
with open(os.path.join(current_location, 'python_test_clone.jsonl'),'w') as f:
    f.write(json.dumps(data))
    
assert 1 == 1
            