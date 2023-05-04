import os
import pathlib

import torch
import pickle

import numpy as np
from sentence_transformers import SentenceTransformer


current_location = pathlib.Path(__file__).parent.resolve()


java_location = os.path.join(current_location, 'java_selected')
ruby_location = os.path.join(current_location, 'ruby_selected')
problems = os.listdir(java_location)

device = torch.device('mps')
model_name = 'microsoft/codebert-base'
model = SentenceTransformer(model_name, device=device)
java_embeddings = {}
ruby_embeddings = {}


for problem in problems:
    if 'DS' in problem:
        continue
            
    java_submissions = [
        open(os.path.join(java_location, problem, s), 'r').read() \
            for s in os.listdir(os.path.join(java_location, problem))
    ]
    
    ruby_submissions = [
        open(os.path.join(ruby_location, problem, s), 'r').read() \
            for s in os.listdir(os.path.join(ruby_location, problem))
    ]
    java_samples_embeddings = model.encode(java_submissions)
    java_problem_embedding = np.average(java_samples_embeddings, axis=0)
    java_embeddings[problem] = java_problem_embedding
    
    ruby_sample_embeddings = model.encode(ruby_submissions)
    ruby_problem_embedding = np.average(ruby_sample_embeddings, axis=0)
    ruby_embeddings[problem] = ruby_problem_embedding


java_file_name = os.path.join(current_location, 'results', 'java_embeddings_dict.pkl')
with open(java_file_name, 'wb') as f:
    pickle.dump(java_embeddings, f)
    
ruby_file_name = os.path.join(current_location, 'results', 'ruby_embeddings_dict.pkl')
with open(ruby_file_name, 'wb') as f:
    pickle.dump(ruby_embeddings, f)

    
    


