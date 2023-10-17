import re

import nltk
from nltk import word_tokenize, Tree

from definitions import FIND_NUMBERS_REG, NUMERICAL_POS_TAG
from models.word_pos_tag import WordPosTag


def extract_word_pos_tags(sentence) -> list[WordPosTag]:
    words_in_string: list[str] = word_tokenize(sentence)
    return [WordPosTag(word=pos_tag[0], pos_tag=pos_tag[1])
            for pos_tag in nltk.pos_tag(words_in_string)]


def revert_word_pos_tags(word_pos_tags: list[WordPosTag]) -> str:
    return ' '.join([word_pos_tag.word for word_pos_tag in word_pos_tags])


def find_Nth_in_chunk(chunk: list[WordPosTag], pos_tag: str, occurrence_number: int) -> str:
    current_occurrence = 0
    for word_pos_tag in chunk:
        if word_pos_tag.pos_tag == pos_tag:
            current_occurrence += 1
            if current_occurrence == occurrence_number:
                return word_pos_tag.word


def chunk_sentence(word_pos_tags: list[WordPosTag], chunk_regex: str) -> list[list[WordPosTag]]:
    chunk_parser = nltk.RegexpParser(chunk_regex)
    chunk_result_tree = chunk_parser.parse(Tree("WordPosTags", word_pos_tags))
    lst_result = []
    for subtree in chunk_result_tree:
        if isinstance(subtree, Tree):
            lst_result.append([child for child in subtree])
    return lst_result


def extract_numbers(word_pos_tags: list[WordPosTag]) -> list[WordPosTag]:
    return [word_pos_tag
            for word_pos_tag in word_pos_tags
            if re.search(FIND_NUMBERS_REG, word_pos_tag.word)]


def validate_number_detection(word_pos_tags: list[WordPosTag]):
    numbers = extract_numbers(word_pos_tags)
    for index in range(len(word_pos_tags)):
        word_pos_tag = word_pos_tags[index]
        if word_pos_tag in numbers and word_pos_tag.pos_tag != NUMERICAL_POS_TAG:
            word_pos_tags[index] = WordPosTag(word_pos_tag.word, NUMERICAL_POS_TAG)

