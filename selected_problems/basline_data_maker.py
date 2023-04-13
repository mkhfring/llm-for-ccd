import os
import re
import json
import pathlib
import random
from abc import ABC, abstractmethod



current_location = pathlib.Path(__file__).parent.resolve()


class BaselineDataMaker(ABC):
    def __init__(self, data_location, output_file, sample_size=1000) -> None:
        self.data_location = data_location
        self.output_file = output_file
        self.sample_size = sample_size
        self.clone_data = []
        self.clone_pairs = []
        self.idx_list = []
        
    def make_data(Self, clone_type=None):
        return NotImplemented
    
    def _make_positive_samples(self, submissions):
        return NotImplemented
    

class CodeBERTData(BaselineDataMaker):
    def __init__(self, data_location, outputfile, sample_size=1000) -> None:
        super().__init__(data_location, outputfile, sample_size)
        
    def make_data(self):
        if os.path.exists(os.path.join(self.output_file, 'data.jsonl')):
            return self
        
        self._make_positive_samples()
        self._make_negative_samples()
        # self._write_json_file()
        # self._write_train_eval_files()
        
    def _make_positive_samples(self):
        return NotImplementedError
    
    def _make_negative_samples():
        return NotImplementedError
    
    def _get_id(self, file_name=None):
        id = re.findall(r'\d+', os.path.basename(file_name))[-1]
        return str(int(id))
    
    def _write_json_file(self):
        # random.shuffle(self.clone_data)
        with open(os.path.join(self.output_file, 'data.jsonl'), 'w') as file:
            for d in self.clone_data:
                json_line = json.dumps(d)
                file.write(json_line + '\n')
    
    def _write_train_eval_files(self):
        # random.shuffle(self.clone_pairs)
        train_end_index = 901028
        dev_test_index_length = 415416
        train = self.clone_pairs[:train_end_index]
        dev = self.clone_pairs[train_end_index:train_end_index + dev_test_index_length]
        test_start_index = train_end_index + dev_test_index_length
        test = self.clone_pairs[-1000:]
        
        with open(os.path.join(self.output_file, 'train.txt'), 'w') as trainfile:
            for train_clone_pair in train:
                trainfile.write(train_clone_pair)
                
        with open(os.path.join(self.output_file, 'dev.txt'), 'w') as devfile:
            for dev_clone_pair in dev:
                devfile.write(dev_clone_pair)
                
        with open(os.path.join(self.output_file, 'test.txt'), 'w') as testfile:
            for test_clone_pair in test:
                testfile.write(test_clone_pair)
        
    def make_test_data(self, test_data_path):
        random.shuffle(self.clone_pairs)
        random.shuffle(self.clone_data)
        with open(test_data_path, 'r') as file:
            test_data = json.loads(file.read())
        
        for element in test_data:
            code1_idx = self._get_id(element['name1'])
            code2_idx = self._get_id(element['name2'])
            self.clone_data.append({'func': element['code1'], 'idx': code1_idx})
            self.clone_data.append({'func': element['code2'], 'idx': code2_idx})
            self.clone_pairs.append(f"{code1_idx}\t{code2_idx}\t{element['label']}\n")
            
        self._write_json_file()
        self._write_train_eval_files()
            
                
        
        
class CrossLanguageCloneDetection(CodeBERTData):
    def __init__(self, data_location, outputfile, sample_size=1000) -> None:
        super().__init__(data_location, outputfile, sample_size)
        
    def make_data(self):
        return super().make_data()
          
    def _make_positive_samples(self):
        if len(self.data_location) !=2:
            raise Exception("Two data locations is required for two different languages")
        
        positive_count = 0
        lang1_problems = os.listdir(self.data_location[0])
        for p in lang1_problems: 
            if '.' in p:
                continue
            
            lang1_submissions = os.listdir(os.path.join(self.data_location[0], p))
            lang2_submissions = os.listdir(os.path.join(self.data_location[1], p))
            for i in range(len(lang1_submissions)):
                for j in range(len(lang2_submissions)):
                    if j - i > 30:
                        break;
                    if positive_count >= self.sample_size/2:
                        break
                    
                    with open(os.path.join(self.data_location[0], p, lang1_submissions[i]), 'r') as f1:
                        code1 = f1.read()
                        
                    with open(os.path.join(self.data_location[1], p, lang2_submissions[j]), 'r') as f2:
                        code2 = f2.read()
                        
                    code1_idx = self._get_id(f1.name)
                    code2_idx = self._get_id(f2.name)
                    self.idx_list.append(int(code1_idx))
                    self.idx_list.append(int(code2_idx))
                        
                    lang1_sample = {'func': code1, 'idx': code1_idx}
                    lang2_sample = {'func': code2, 'idx': code2_idx}
                    
                    self.clone_data.append(lang1_sample)
                    self.clone_data.append(lang2_sample)
                    self.clone_pairs.append(f"{code1_idx}\t{code2_idx}\t1\n")
                    positive_count = positive_count + 1
                    
        return self
                    
    def _make_negative_samples(self):
        negative_count = 0
        lang1_problems = os.listdir(self.data_location[0])
        lang1_problems = [p for p in lang1_problems if '.' not in p]
        for i in range(len(lang1_problems)):
            for j in range(i+1, len(lang1_problems)):
                if negative_count >= self.sample_size/2:
                    break
            
                problem1 = lang1_problems[i]
                problem2 = lang1_problems[j]

                if problem1 == problem2:
                    continue
                
                p1_sub = os.listdir(os.path.join(self.data_location[0], problem1))
                p2_sub = os.listdir(os.path.join(self.data_location[1], problem2))
                
                for lang1_index in range(len(p1_sub)):
                    for lang2_index in range(len(p2_sub)):
                         
                        with open(os.path.join(self.data_location[0], problem1, p1_sub[lang1_index]), 'r') as f1:
                            code1 = f1.read()
                        
                        with open(os.path.join(self.data_location[1], problem2, p2_sub[lang2_index]), 'r') as f2:
                            code2 = f2.read()
        
                        code1_idx = self._get_id(f1.name)
                        code2_idx = self._get_id(f2.name)
                        self.idx_list.append(int(code1_idx))
                        self.idx_list.append(int(code2_idx))
                        
                        lang1_sample = {'func': code1, 'idx': code1_idx}
                        lang2_sample = {'func': code2, 'idx': code2_idx}
                    
                        self.clone_data.append(lang1_sample)
                        self.clone_data.append(lang2_sample)
                        self.clone_pairs.append(f"{code1_idx}\t{code2_idx}\t0\n")
                        negative_count = negative_count + 1
                    
        return self
                    
                
if __name__ == "__main__":
    
    cross_language_data = CrossLanguageCloneDetection(
        [
            os.path.join(current_location, 'train_java_selected'),
            os.path.join(current_location, 'ruby_selected'),
        ],
        os.path.join(current_location, 'clone_data'),
        sample_size=1732000
    )
    cross_language_data.make_data()
    cross_language_data.make_test_data(os.path.join(current_location, 'ruby_java_test_clone3.jsonl'))