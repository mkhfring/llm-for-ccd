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

java_new_problems = os.listdir(java_new)
java_selected_problems = os.listdir(java_selected)
for p in java_new_problems:
    if p in java_selected_problems:
        assert 1 == 1
assert 1 == 1