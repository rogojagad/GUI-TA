import json
import pickle
import sys
import string
import spacy
from pprint import pprint
from spellchecker import SpellChecker
from dependency_parser.standford_dependency_parser import StandfordDependencyParser
from dependency_parser.spacy_parser import SpacyParser


class Preprocessor:
    def __init__(self):
        self.standford_dependency_parser = StandfordDependencyParser()
        self.spacy_parser = SpacyParser()
        self.nlp = spacy.load("en_core_web_sm")

    def tokenize_and_pos_tagging(self, sentence):
        tokens = []
        pos_tag_labels = []

        translator = str.maketrans("", "", string.punctuation)
        sentence = sentence.strip("\n")

        docs = self.nlp(sentence.translate(translator))

        for idx, doc in enumerate(docs):
            tokens.append(doc.text)
            pos_tag_labels.append(doc.pos_)

        return tokens, pos_tag_labels

    def get_word_label(self, word, words_data, list_of_targets):
        for targets in list_of_targets:
            if word in targets:
                if targets.index(word) > 0:
                    if words_data[-1][1] == "B" or words_data[-1][1] == "I":
                        return "I"
                elif targets.index(word) == 0:
                    return "B"
        else:
            return "O"

    def get_target(self, targets):
        splitted_targets = []

        for target in targets:
            # print(target.split(' '))
            splitted_targets.append(target.split(" "))

        return splitted_targets

    def start_preprocess(self, sentence):
        labelling_result = []

        dependency_parsing_result = self.standford_dependency_parser.parse(sentence)

        spacy_parsing_result = self.spacy_parser.parse(sentence)

        tokenized, pos_tag_labels = self.tokenize_and_pos_tagging(sentence)

        headword_pair = self.extract_headword(tokenized, dependency_parsing_result)

        governor_relation_dict = self.standford_dependency_parser.get_governor_relation(
            tokenized, dependency_parsing_result
        )

        dependent_relation_dict = self.standford_dependency_parser.get_dependent_relation(
            tokenized, dependency_parsing_result
        )

        for token, pos_label in zip(tokenized, pos_tag_labels):
            if token in governor_relation_dict:
                governor_relation = governor_relation_dict[token]
            else:
                governor_relation = None

            if token in dependent_relation_dict:
                dependent_relation = dependent_relation_dict[token]
            else:
                dependent_relation = None

            labelling_result.append(
                (token, pos_label, governor_relation, dependent_relation)
            )

        return labelling_result, headword_pair, spacy_parsing_result

    def extract_headword(self, tokenized, dependency_parsing_result):
        headword_result = []

        for token in tokenized:
            match_item = 0

            for item in dependency_parsing_result:
                if item[2][0] == token:
                    match_item = dependency_parsing_result.index(item)
                    headword_result.append((token, item[0][0], item[0][1]))
                    break
            else:
                headword_result.append((token, None, None))

            if len(dependency_parsing_result) != 0:
                del dependency_parsing_result[match_item]

        return headword_result


if __name__ == "__main__":
    preprocessor = Preprocessor()

    pprint(preprocessor.start_preprocess("The food is very good."))

