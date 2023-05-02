import os
import re
import json
import pathlib
from abc import ABC, abstractmethod


current_location = pathlib.Path(__file__).parent.resolve()


class MissedSamples(ABC):
    def __init__(self, missing_ids_file_path,  data_file_path) -> None:
        self.id_path = missing_ids_file_path
        self.data_path = data_file_path
        self.positive_samples = []
        self.negative_samples = []
        self.missing_positive_problems = None
        self.missing_negative_problems = None
        self.missing_ids = self._read_missing_ids()
        
    def _read_missing_ids(self):
        ids = []
        with open(self.id_path, 'r') as f:
            for line in f.readlines():
                ids.append(int(line))
                
        return ids
        
    def get_missing_problems(self):
        data = self._read_data()
        for id in self.missing_ids:
            for sample in data:
                if id == sample['id']:
                    if sample['label'] == 1:
                        self.positive_samples.append(sample)
                    else:
                        self.negative_samples.append(sample)
                        
        positive_problems = self._find_positive_problems()
        negative_problems = self._find_negative_problems()
        
        
    @abstractmethod    
    def _find_positive_problems(self):
        pass
    
    @abstractmethod    
    def _find_negative_problems(self):
        pass
                        
             
    def _read_data(self):
        data = None
        with open(self.data_path, 'r') as f:
            for line in f.readlines():
                data = json.loads(line)
            
        return data
    
    @property
    def get_missing_postive_problems(self):
        return self.missing_positive_problems
    
    @property
    def get_missing_negative_problems(self):
        return self.missing_negative_problems
    
    
class JavaMissingSamples(MissedSamples):
    def __init__(self, missing_ids_file_path, data_file_path) -> None:
        super().__init__(missing_ids_file_path, data_file_path)
        self.location = os.path.join(current_location, 'java_selected')
        self.problems = os.listdir(self.location)
        
        
    def _find_positive_problems(self):
        missing_problems = []
        for problem in self.problems:
            if 'DS' in problem:
                continue
            
            submissions = [
                open(os.path.join(self.location, problem, s), 'r').read() \
                    for s in os.listdir(os.path.join(self.location, problem))
            ]
            for sample in self.positive_samples:
                if sample['code2'] in submissions:
                    missing_problems.append(problem)
            
        self.missing_positive_problems = missing_problems
        
    def _find_negative_problems(self):
        negative_problmes = {}
        for problem in self.problems:
            if 'DS' in problem:
                continue
            
            submissions = [
                open(os.path.join(self.location, problem, s), 'r').read() \
                    for s in os.listdir(os.path.join(self.location, problem))
            ]
            for sample in self.negative_samples:
                if sample['code1'] in submissions or sample['code2'] in submissions:
                    if sample['id'] in negative_problmes:
                        negative_problmes[sample['id']].append(problem)
                    else:
                        negative_problmes[sample['id']] = [problem]
                        
        self.missing_negative_problems = negative_problmes
                     
        
class RubyJavaMissingSamples(MissedSamples):
    def __init__(self, missing_ids_file_path, data_file_path) -> None:
        super().__init__(missing_ids_file_path, data_file_path)
        self.java_location = os.path.join(current_location, 'java_selected')
        self.ruby_location = os.path.join(current_location, 'ruby_selected')
        self.problems = os.listdir(self.java_location)
        
        
    def _find_positive_problems(self):
        missing_problems = []
        for problem in self.problems:
            if 'DS' in problem:
                continue
            
            submissions = [
                open(os.path.join(self.java_location, problem, s), 'r').read() \
                    for s in os.listdir(os.path.join(self.java_location, problem))
            ]
            for sample in self.positive_samples:
                if sample['code1'] in submissions:
                    missing_problems.append(problem)
                    
        self.missing_positive_problems = missing_problems
        
    def _find_negative_problems(self):
        negative_problmes = {}
        for problem in self.problems:
            if 'DS' in problem:
                continue
            
            java_submissions = [
                open(os.path.join(self.java_location, problem, s), 'r').read() \
                    for s in os.listdir(os.path.join(self.java_location, problem))
            ]
            ruby_submissions = [
                open(os.path.join(self.ruby_location, problem, s), 'r').read() \
                    for s in os.listdir(os.path.join(self.ruby_location, problem))
            ]
            for sample in self.negative_samples:
                if sample['code1'] in java_submissions or sample['code2'] in ruby_submissions:
                    if sample['id'] in negative_problmes:
                        negative_problmes[sample['id']].append(problem)
                    else:
                        negative_problmes[sample['id']] = [problem]
                        
        self.missing_negative_problems = negative_problmes
        

    
        

class MissingProblemsFactory:
        
    @abstractmethod
    def missing_problems_creation(missing_id_path, data_file_path, type):
        
        if type == 'java-java':
    
            return JavaMissingSamples(missing_id_path, data_file_path)
        else:
            return RubyJavaMissingSamples(missing_id_path, data_file_path)
        
        
if __name__ == "__main__":
    java_missing_samples = MissingProblemsFactory.missing_problems_creation(
        os.path.join(current_location, 'results', 'java_java_missing_index.txt'),
        os.path.join(current_location, 'java_test_clone_2.jsonl'),
        type='java-java'
    )
    java_missing_samples.get_missing_problems()
    
    java_ruby_missing_samples = MissingProblemsFactory.missing_problems_creation(
        os.path.join(current_location, 'results', 'java_ruby_missing_index.txt'),
        os.path.join(current_location, 'ruby_java_test_clone2.jsonl'),
        type='ruby-java'
    )
    java_ruby_missing_samples.get_missing_problems()
    for p in java_missing_samples.get_missing_postive_problems:
        if p in java_ruby_missing_samples.get_missing_postive_problems:
            print(p)
    
    common_missing_negative_pair = []
    for key, value in java_missing_samples.get_missing_negative_problems.items():
        for k, v in java_ruby_missing_samples.get_missing_negative_problems.items():
            if value == v:
                if value not in common_missing_negative_pair:
                    common_missing_negative_pair.append(value)
                
    assert 1 == 1
        