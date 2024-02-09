# Investigating the Efficacy of Large Language Models for Code Clone Detection

This repository contains all source code and data associated with the research paper entitled ["Investigating the Efficacy of Large Language Models for Code Clone Detection"](https://arxiv.org/abs/2401.13802) 

- All source codes and data files are inside the selected_problems directory.
- The main codes to make requests and analyse the results exist in `selected_problems/chatgpt.py`. To make the requests the Open-ai access key should be inserted in a text file. Then, the path of this access key should be specify inside the `read_api_key` fucntion inside `ChatGPTRequest` class. This class is located inside `selected_problems/chatgpt.py`. 
- Jsonl files inside `selected_problems` include the data that is used for our experiments. 
- The `baseline_data_maker.py` includes the source code to generate datasets for baselines experiments.


## Citation

```
@article{khajezade2024investigating,
  title={Investigating the Efficacy of Large Language Models for Code Clone Detection},
  author={Khajezade, Mohamad and Wu, Jie JW and Fard, Fatemeh Hendijani and Rodr{\'\i}guez-P{\'e}rez, Gema and Shehata, Mohamed Sami},
  journal={arXiv preprint arXiv:2401.13802},
  year={2024}
}
```
