from typing import List, Any, Tuple, Dict
import json
import os


def count_individuals(elements: List[Any]) -> List[Tuple[Any, int]]:
    unique_elements: List[Any] = list(set(elements))
    count_per_element: List[Tuple[Any, int]] = []
    for element in unique_elements:
        count_per_element.append((
            element, elements.count(element)
        ))
    return count_per_element

def read_histories(data_dir) -> List[Dict]:
    """Reads streaming histories from files in given data directory and merges them"""
    merged_histories: List[Dict] = []
    for file in os.listdir(data_dir):
        with open(os.path.join(data_dir, file), "r", encoding="UTF-8") as file:
            history: List[Dict] = json.loads(file.read())
            merged_histories = merged_histories + history
    
    return merged_histories