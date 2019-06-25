from analyzer.base_analyzer import BaseAnalyzer

from .value_getter.bing_liu_value_getter import BingLiuLexiconValueGetter
from .value_getter.gi_lexicon_value_getter import GeneralInquirerLexiconValueGetter
from .value_getter.mpqa_value_getter import MPQALexiconValueGetter
from .value_getter.sentiwordnet_value_getter import SentiWordNetValueGetter

from .distance_getter.dependency_path_distance_getter import (
    DependencyPathDistanceGetter,
)
from .distance_getter.token_distance_getter import TokenDistanceGetter

from pprint import pprint


class SentimentAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.bing_liu_value_getter = BingLiuLexiconValueGetter()
        self.gi_lexicon_value_getter = GeneralInquirerLexiconValueGetter()
        self.mpqa_value_getter = MPQALexiconValueGetter()
        self.sentiwordnet_value_getter = SentiWordNetValueGetter()

        self.token_distance_getter = TokenDistanceGetter()

        self.negation_words = ["not", "no", "never", "nt"]

        self.needed_pos_label = ["ADJ", "ADV", "VERB", "DET", "NOUN"]

        self.current_target_words_list = list()

        print("Sentiment Analyzer instantiated....")

    def create_graph_data(self, parsing_result):
        self.dependency_path_distance_getter = DependencyPathDistanceGetter(
            parsing_result
        )

    def analyze(self, sentence_data):
        self.token_distance_getter.set_sentence(sentence_data)
        self.current_target_words_list = self.token_distance_getter.aspect_words_list

        target_counter = 0
        result = dict()

        for idx, data in enumerate(sentence_data):
            if data[2] == "B":

                backward_value = self.analyze_backward(sentence_data, idx)
                forward_value = self.analyze_forward(sentence_data, idx)
                total_polarity_value = backward_value + forward_value

                if total_polarity_value > 0:
                    polarity = "positive"
                elif total_polarity_value < 0:
                    polarity = "negative"
                else:
                    polarity = "neutral"

                result[self.current_target_words_list[target_counter]] = polarity

                target_counter += 1

        return result

    def analyze_backward(self, doc, target_idx):
        i = target_idx - 1
        target_word = doc[target_idx][0]
        total_value = 0

        while i >= 0:
            opinion_word = doc[i][0]

            lexicon_value = self.get_lexicon_value_sum(opinion_word.lower(), doc[i])

            distance_value = self.get_distance_value_sum(
                target_word, target_idx, opinion_word, i
            )

            value = lexicon_value / distance_value

            if self.check_negation(i, doc):
                value *= -1

            total_value += value

            i -= 1

        return total_value

    def analyze_forward(self, doc, target_idx):
        total_value = 0
        target_word = doc[target_idx][0]

        for i in range(target_idx + 1, len(doc)):
            if doc[i][2] != "I":
                opinion_word = doc[i][0]

                lexicon_value = self.get_lexicon_value_sum(opinion_word.lower(), doc[i])

                distance_sum = self.get_distance_value_sum(
                    target_word, target_idx, opinion_word, i
                )

                value = lexicon_value / distance_sum

                if self.check_negation(i, doc):
                    value *= -1

                total_value += value
        return total_value

    def get_lexicon_value_sum(self, opinion_word, token_data):
        gi_lexicon_value = self.gi_lexicon_value_getter.get_value(opinion_word.lower())

        mpqa_value = self.mpqa_value_getter.get_value(opinion_word.lower())

        sentiword_net_value = self.sentiwordnet_value_getter.get_value(token_data)

        bing_liu_value = self.bing_liu_value_getter.get_value(opinion_word.lower())

        return bing_liu_value + sentiword_net_value + mpqa_value + gi_lexicon_value

    def get_distance_value_sum(self, target_word, target_idx, opinion_word, i):
        dependency_distance = self.dependency_path_distance_getter.get_distance_value(
            target_word.lower(), target_idx, opinion_word.lower(), i
        )

        return dependency_distance

    def check_negation(self, i, doc):
        j = 1

        while j <= 3:
            idx = i + j
            if idx < len(doc):
                if doc[idx][0] in self.negation_words:
                    return True
            else:
                break

            j += 1

        j = 1

        while j <= 3:
            idx = i - j

            if idx >= 0:
                if doc[idx][0] in self.negation_words:
                    return True
            else:
                break

            j += 1


if __name__ == "__main__":
    analyzer = SentimentAnalyzer()

    analyzer.create_graph_data(
        [
            ("food-1", "the-0"),
            ("is-2", "food-1"),
            ("is-2", "good-4"),
            ("is-2", ".-5"),
            ("good-4", "very-3"),
        ]
    )

    pprint(
        analyzer.analyze(
            [
                ("The", "DET", "O"),
                ("food", "NOUN", "B"),
                ("is", "VERB", "O"),
                ("very", "ADV", "O"),
                ("good", "ADJ", "O"),
            ]
        )
    )
