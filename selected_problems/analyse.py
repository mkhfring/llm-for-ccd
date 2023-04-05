import os
import re
import json
import pathlib

from sklearn.metrics import precision_score, recall_score, f1_score


current_location = pathlib.Path(__file__).parent.resolve()


class Analyser:
    """
    A class to analyze and extract results from test and report files.
    Attributes:
        test_data (dict): A dictionary containing the test data.
        report_file (str): The path to the report file.
        results (dict): A dictionary containing the extracted results.
    """

    def __init__(self, test_file, report_file) -> None:
        """
        Initializes the Analyser class with the test and report files.

        Args:
            test_file (str): The path to the test data file.
            report_file (str): The path to the report file.
        """
        self.precision = None
        self.recall = None
        self.f1_score = None
        self.report_file = report_file
        self.test_data = self.read_data(test_file)
        self.results = self._extract_results()
        
    def read_data(self, data_file):
        """
        Reads data from the specified data file and returns it as a dictionary.

        Args:
            data_file (str): The path to the data file.

        Returns:
            dict: The data as a dictionary.
        """
        with open(data_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                
        return data
    
    def _extract_results(self):
        """
        Extracts results from the report file and returns them as a dictionary.

        Returns:
            dict: The extracted results as a dictionary.
        """
        pure_results = self._read_lines(self.report_file)
        result = {}
        for data in pure_results:
            try:
                data_id = int(re.search(r"Data Id (\d+):", data).group(1))
            except:
                assert 1 == 1
                
            if 'yes' in data.lower():
                data_value = 1
            elif 'no' in data.lower():
                data_value = 0
            else:
                assert 1 == 1
            
            result[data_id] = data_value
            
        return result

    def _read_lines(self, file_path):
        """
        Reads lines from the specified file and returns a list of unprocessed results.

        Args:
            file_path (str): The path to the file.

        Returns:
            list: A list of unprocessed results.
        """
        unprocessed_results = []
        with open(file_path, 'r') as f:
            for line in f:
                if '**' in line:
                    block_begin = ''
                
                block_begin = block_begin + line.strip()
                
                if '++' in line:
                    unprocessed_results.append(block_begin) 
            
        return unprocessed_results
    
    def _extract_ground_truth_labels(self):
        samples_label = [{sample['id']: sample['label']} for sample in self.test_data]
        return samples_label
    
    def compute_metrics(self, description = None, save_to_file=False):
        ground_truth_labels = []
        predictions_labels = []
        
        for element in self.ground_truth:
            key = list(element.keys())[0]

            if key in self.predicted_results:
                ground_truth_labels.append(element[key])
                predictions_labels.append(self.predicted_results[key])
        
        self.precision = precision_score(ground_truth_labels, predictions_labels, average='macro')
        self.recall = recall_score(ground_truth_labels, predictions_labels, average='macro')
        self.f1_score = f1_score(ground_truth_labels, predictions_labels, average='macro') 
        if save_to_file:
            self.write_results_to_file(description)
            
    def write_results_to_file(self, description):
        file_description_text = f"{description}\n\n"
        file_description_text = file_description_text + f"F1 score: {self.f1_score}\n"
        file_description_text = file_description_text + f"Precision: {self.precision}\n"
        file_description_text = file_description_text + f"Recall: {self.recall}\n"
        file_name = '_'.join(description.split(" "))+'.txt'
        with open(os.path.join(current_location, 'results', file_name), "w") as file:
            file.write(file_description_text)
        
        
    @property
    def predicted_results(self):
        """
        Returns the extracted results as a dictionary.

        Returns:
            dict: The extracted results as a dictionary.
        """
        return self.results
    
    @property
    def ground_truth(self):
        """
        Returns the extracted results as a dictionary.

        Returns:
            dict: The extracted results as a dictionary.
        """
        return self._extract_ground_truth_labels()
    
    

if __name__ == '__main__':
    analyser = Analyser(
        os.path.join(current_location, 'java_test_clone_2.jsonl'),
        os.path.join(current_location, 'results', 'results_java_01.txt')
    )
    analyser.compute_metrics()
    assert analyser.predicted_results is not None