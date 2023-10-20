def __file_rows(arr_lines):
    return [item.replace('\n', "") for item in arr_lines]


def parse_file(path_to_file: str) -> list[str]:
    with open(path_to_file, 'r') as adjectives_txt_file:
        return __file_rows(adjectives_txt_file)
