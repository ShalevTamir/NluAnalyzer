from collections import namedtuple
from typing import List

import nltk
from nltk import word_tokenize, WordNetLemmatizer

from models.word_pos_tag import WordPosTag


class RangeAnalyzer:
    def _extract_parameter_name(self, pos_tags_lst: list[WordPosTag], index: int):
        print(pos_tags_lst)
        if pos_tags_lst[index].word == "parameter":
            index += 1
        # remove word 'parameter'
        pos_tags_lst = [pos_tag for pos_tag in pos_tags_lst if pos_tag.word.lower() != 'parameter']
        index -= 1
        parameter_name = ""
        for offset in range(2):
            if index + offset < len(pos_tags_lst):
                pos_tag_word = pos_tags_lst[index + offset]
                if 'NN' in pos_tag_word.pos_tag:
                    parameter_name += f' {pos_tag_word.word}'

        return None if parameter_name == "" else parameter_name[1:]

    def extract_range(self, str_to_analyze):
        words_in_string: list[str] = word_tokenize(str_to_analyze)
        pos_tags: list[WordPosTag] = [WordPosTag(word=pos_tag[0], pos_tag=pos_tag[1])
                                      for pos_tag in nltk.pos_tag(words_in_string)]

        for index in range(len(pos_tags)):
            param_name = self._extract_parameter_name(pos_tags, index)
            if param_name:
                print(param_name)
                return


RangeAnalyzer().extract_range("flap position greater than 50 and smaller than 100")
