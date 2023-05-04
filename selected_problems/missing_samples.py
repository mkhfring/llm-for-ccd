import os
import pickle
import json
import pathlib
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import lizard


current_location = pathlib.Path(__file__).parent.resolve()


class ComplexityComputation:
    def __init__(self, problems_path, complexity_file_path) -> None:
        
        self.path = problems_path
        self.problems  = [p for p in os.listdir(self.path) if '.DS' not in p]
        self.problem_accept_rate = self.get_acceptance_rate()
        self.complexity_file_path = complexity_file_path
        if not os.path.exists(self.complexity_file_path):
            self.complexity = self._compute_complexity()
        else:
            self.complexity = self._load_complexity()
            
            
    def _load_complexity(self):
        with open(self.complexity_file_path, 'rb') as file:
            data = pickle.load(file)
            
        return data
        
        
    def _compute_complexity(self):
        problems = os.listdir(self.path)
        problem_complexity = {}
        problems = [p for p in problems if '.DS' not in p]
        for problem in problems:
            accepted_submissions = os.listdir(os.path.join(self.path, problem))
            accepted_submissions_path = [os.path.join(self.path, problem, s) for s in accepted_submissions]
            problem_complexity[problem] = self._average_complexity(
                accepted_submissions_path
            )
            
        self._write_complexity_in_file(problem_complexity)
        return problem_complexity
        
    def _write_complexity_in_file(self, complexity):
        with open(self.complexity_file_path, 'wb') as f:
            pickle.dump(complexity, f)
            
    
    def get_acceptance_rate(self):
        problem_accept_rate = {}
        selected_dir = os.path.dirname(self.path)
        for problem in self.problems:
            problem_meta_data_path = os.path.join(
                os.path.dirname(selected_dir),
                'metadata',
                f'{problem}.csv'
            )
            meta_data = pd.read_csv(problem_meta_data_path)
            problem_accepted_submissions = list(meta_data.loc[meta_data['status'] == 'Accepted']['submission_id'])
            submissions = os.listdir(os.path.join(self.path, problem))
            problem_accept_rate[problem] = len(submissions) / len(problem_accepted_submissions)
            
        return problem_accept_rate
    
    def _average_complexity(self, submissions):
        complexity = []
        for sub in submissions:
            result = lizard.analyze_file(sub)
            for func_result in result.function_list:
                complexity.append(func_result.cyclomatic_complexity)
        
        return sum(complexity) / len(complexity)
    
    def average_acceptance_rate(self):
        rate = list(self.get_accept_ratio.values())
        return sum(rate) / len(rate)
    
    def average_complexity(self):
        rate = list(self.complexity.values())
        return sum(rate) / len(rate)
    
    @property
    def get_complexity(self):
        return self.complexity
    
    @property
    def get_accept_ratio(self):
        return self.problem_accept_rate


class SimilarityComputation:
    def __init__(self, common_missing_pairs, common_correct_pairs, ruby_embedding_path, java_embedding_path) -> None:
        self.missing_pairs = common_missing_pairs
        self.correct_pairs = common_correct_pairs
        self.ruby_path = ruby_embedding_path
        self.java_path = java_embedding_path
        self.ruby_embeddings = self._read_embedding_file('ruby')
        self.java_embeddings = self._read_embedding_file('java')
        self.correct_samples_similarity = self._cosign_similarity(common_correct_pairs)
        self.missing_samples_similarity = self._cosign_similarity(common_missing_pairs)
        assert 1 == 1
        
    def _cosign_similarity(self, common_pairs):
        similarity = []
        for pair in common_pairs:
            dot_product = np.dot(
                self.java_embeddings[pair[0]],
                self.ruby_embeddings[pair[1]]
            )
            norm_embedding1 = np.linalg.norm(self.java_embeddings[pair[0]])
            norm_embedding2 = np.linalg.norm(self.ruby_embeddings[pair[1]])
            similarity.append(dot_product / (norm_embedding1 * norm_embedding2))
            
        return sum(similarity) / len(similarity)
    
    def _read_embedding_file(self, language):
        if language =='ruby':
            file = self.ruby_path
        else:
            file = self.java_path
            
        with open(file, 'rb') as file:
            data = pickle.load(file)
            
        return data
        


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
                        
        self._find_positive_problems()
        self._find_negative_problems()
        
        
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
        
        
def get_unique_set_of_problems(negative_samples):
    problems = set()
    for value in negative_samples.values():
        problems.add(value[0])
        problems.add(value[1])
        
    return problems
 
        
# Starting the computations
def calculate_average_complexity(metric, data):
    rate = []
    for element in data:
        if isinstance(element, str):
            rate.append(metric[element])
            
        else:
            if metric[element[0]] > metric[element[1]]:
                rate.append(metric[element[0]])
            else:
                rate.append(metric[element[1]])
            
    return sum(rate) / len(rate)

def calculate_average_acceptance(metric, data):
    rate = []
    for element in data:
        if isinstance(element, str):
            rate.append(metric[element])
        
        else:
            if metric[element[0]] < metric[element[1]]:
                rate.append(metric[element[0]])
            else:
                rate.append(metric[element[1]])
            
    return sum(rate) / len(rate)
        
if __name__ == "__main__":
    
    complexity_metrics = ComplexityComputation(
        os.path.join(current_location, 'java_selected'),
        os.path.join(current_location, 'results', 'complexity.pkl')
    )
    average_acceptance = complexity_metrics.average_acceptance_rate()
    average_complexity = complexity_metrics.average_complexity()
    assert 1 == 1
    
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
    positive_average_accept = calculate_average_acceptance(complexity_metrics.get_accept_ratio, java_ruby_missing_samples.get_missing_postive_problems)
    positive_average_complexity = calculate_average_complexity(complexity_metrics.get_complexity, java_ruby_missing_samples.get_missing_postive_problems)

    for p in java_missing_samples.get_missing_postive_problems:
        if p in java_ruby_missing_samples.get_missing_postive_problems:
            print(p)
            
    java_positive_missing_accept_rate = complexity_metrics.get_accept_ratio[p]
    java_positive_missing_complexity = complexity_metrics.get_complexity[p]
    assert 1 == 1
    
    java_java_missing_negative_problems = get_unique_set_of_problems(
        java_missing_samples.get_missing_negative_problems
    )
    java_ruby_missing_negative_problems = get_unique_set_of_problems(
        java_ruby_missing_samples.get_missing_negative_problems
    )
    common_missing_problems = []
    if len(java_java_missing_negative_problems) > len(java_ruby_missing_negative_problems):
        iteration_set = java_ruby_missing_negative_problems
        other_set = java_java_missing_negative_problems
    else:
        iteration_set = java_java_missing_negative_problems
        other_set = java_ruby_missing_negative_problems
        
    for problem in iteration_set:
        if problem in other_set:
            common_missing_problems.append(problem)
            
    assert 1 == 1
        
    
    common_missing_negative_pair = []
    for key, value in java_missing_samples.get_missing_negative_problems.items():
        for k, v in java_ruby_missing_samples.get_missing_negative_problems.items():
            if value == v:
                if value not in common_missing_negative_pair:
                    common_missing_negative_pair.append(value)
                    
                  
    #For Correct Problems
    #TODO: Change the name to reflect both missing and correct problems
    java_correct_samples = MissingProblemsFactory.missing_problems_creation(
        os.path.join(current_location, 'results', 'java_java_correct_index.txt'),
        os.path.join(current_location, 'java_test_clone_2.jsonl'),
        type='java-java'
    )
    java_correct_samples.get_missing_problems()
    
    java_ruby_correct_samples = MissingProblemsFactory.missing_problems_creation(
        os.path.join(current_location, 'results', 'java_ruby_correct_index.txt'),
        os.path.join(current_location, 'ruby_java_test_clone2.jsonl'),
        type='ruby-java'
    )
    java_ruby_correct_samples.get_missing_problems()
    
    java_java_correct_negative_problems = get_unique_set_of_problems(
         java_correct_samples.get_missing_negative_problems
    )
    common_correct_negative_pair = []
    for key, value in java_correct_samples.get_missing_negative_problems.items():
        for k, v in java_ruby_correct_samples.get_missing_negative_problems.items():
            if value == v:
                if value not in common_correct_negative_pair:
                    common_correct_negative_pair.append(value)
                    
    negative_average_accept = calculate_average_acceptance(complexity_metrics.get_accept_ratio, common_missing_negative_pair)
    negative_average_complexity = calculate_average_complexity(complexity_metrics.get_complexity, common_missing_negative_pair)
    assert 1 == 1
    
                    
    # sc = SimilarityComputation(
    #     common_missing_negative_pair,
    #     common_correct_negative_pair,
    #     os.path.join(current_location, 'results', 'ruby_embeddings_dict.pkl'),
    #     os.path.join(current_location, 'results', 'java_embeddings_dict.pkl')
    # )

                    
    
                
        