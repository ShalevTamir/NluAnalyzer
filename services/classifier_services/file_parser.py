from typing import List


PATH_TO_DOCUMENTS = 'documents/'


def _preprocess(arr_lines):
    return [item.replace('\n', "") for item in arr_lines]


def parse_file(file_name: str) -> List[str]:
    with open(PATH_TO_DOCUMENTS + file_name + ".txt", 'r') as adjectives_txt_file:
        return _preprocess(adjectives_txt_file)
