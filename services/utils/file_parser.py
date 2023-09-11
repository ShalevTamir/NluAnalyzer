from typing import List




def _preprocess(arr_lines):
    return [item.replace('\n', "") for item in arr_lines]


def parse_file(path_to_file: str) -> List[str]:
    with open(path_to_file, 'r') as adjectives_txt_file:
        return _preprocess(adjectives_txt_file)
