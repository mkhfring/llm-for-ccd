# Investigating the Efficacy of Large Language Models for Code Clone Detection

This repository contains all source code and data associated with the research paper entitled ["Investigating the Efficacy of Large Language Models for Code Clone Detection"](https://arxiv.org/abs/2401.13802) 

## Overview
Large Language Models (LLMs) have demonstrated remarkable success in various natural language processing and software engineering tasks, such as code generation. The LLMs are mainly utilized in the prompt-based zero/few-shot paradigm to guide the model in accomplishing the task. GPT-based models are one of the popular ones studied for tasks such as code comment generation or test generation. These tasks are generative tasks. However, there is limited research on the usage of LLMs for non-generative tasks such as classification using the prompt-based paradigm. In this preliminary exploratory paper, we investigated the applicability of LLMs for Code Clone Detection (CCD), a non-generative task. By building a mono-lingual and cross-lingual CCD dataset derived from CodeNet, we first investigated two different prompts using ChatGPT to detect Type-4 code clones in Java-Java and Java-Ruby pairs in a zero-shot setting. We then analyzed to understand the strengths and weaknesses of ChatGPT in CCD. ChatGPT surpasses the baselines in cross-language CCD attaining an F1-score of 0.877 and achieving comparable performance to fully fine-tuned models for mono-lingual CCD, with an F1-score of 0.878. Also, the prompt and the difficulty level of the problems have an impact on the performance of ChatGPT.

## Run

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
