from typing import List, Any, Tuple


def count_individuals(elements: List[Any]) -> List[Tuple[Any, int]]:
    unique_elements: List[Any] = list(set(elements))
    count_per_element: List[Tuple[Any, int]] = []
    for element in unique_elements:
        count_per_element.append((
            element, elements.count(element)
        ))
    return count_per_element
