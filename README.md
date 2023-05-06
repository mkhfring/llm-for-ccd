# Exploiting Large Language Models for Non-Generative Code Classification Tasks

This repository contains all source code and data associated with the research paper entitled "Leveraging Large Language Models for Non-Generative Code Classification Tasks."

- All source codes and data files are inside the selected_problems directory.
- The main codes to make requests and analyse the results exist in `selected_problems/chatgpt.py`. To make the requests the Open-ai access key should be inserted in a text file. Then, the path of this access key should be specify inside the `read_api_key` fucntion inside `ChatGPTRequest` class. This class is located inside `selected_problems/chatgpt.py`. 
- Jsonl files inside `selected_problems` include the data that is used for our experiments. 
- The `baseline_data_maker.py` includes the source code to generate datasets for baselines experiments.
