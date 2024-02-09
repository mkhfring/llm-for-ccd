import os
import pathlib
import shutil
import random

import pandas as pd

data_location = "/Users/mohamadkhajezade/workspace/chatGPT/codenet_data_mini"

current_location = pathlib.Path(__file__).parent.resolve()
java_selected = os.path.join(current_location, 'java_selected')
ruby_selected = os.path.join(current_location, 'ruby_selected')
java = os.path.join(data_location, 'Java')
main_java_problems = os.listdir(java)
java_new = os.path.join(current_location, 'train_java_selected')

ruby_selected_problems = os.listdir(ruby_selected)
java_selected_problems = os.listdir(java_selected)
ruby_problems_not_in_java = [p for p in ruby_selected_problems if p not in java_selected_problems]

selected_indexes = random.sample(ruby_problems_not_in_java, 100)
for p in selected_indexes:
    meta_data = pd.read_csv(os.path.join(data_location, 'Project_CodeNet/metadata', f'{p}.csv'))
    problem_accepted_submissions = list(meta_data.loc[meta_data['status'] == 'Accepted']['submission_id'])
    all_submissions = os.listdir(os.path.join(java, p))
    if len(all_submissions) < 10:
        continue
    
    java_accepted = [s for s in all_submissions if s[:-5] in problem_accepted_submissions]
    if len(java_accepted) > 0:
        if not os.path.exists(os.path.join(java_new, p)):
            os.makedirs(os.path.join(java_new, p))
    else:
        continue
    
    for s in java_accepted:
        if not os.path.exists(os.path.join(java_new, p, s)):
            assert 1 == 1
            shutil.copyfile(os.path.join(java, p, s), os.path.join(java_new, p, s))
            assert 1 == 1 