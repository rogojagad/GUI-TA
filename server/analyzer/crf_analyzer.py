import pycrfsuite
from analyzer.base_analyzer import BaseAnalyzer
from pprint import pprint


class CRFAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.tagger = pycrfsuite.Tagger(self.data_dir + "crf.model")
        print("CRF Analyzer instantiated....")

    def analyze(self, token_with_data, feature_data):
        self.tagger.open(self.data_dir + "crf.model")

        result = []

        for xseq in feature_data:
            result = self.tagger.tag(xseq)

        return self.make_label_word_pair(result, token_with_data)

    def make_label_word_pair(self, result, token_with_data):
        word_label_pair = list()

        for label, word in zip(result, token_with_data):
            word_label_pair.append((word[0], word[1], label))

        return word_label_pair


if __name__ == "__main__":
    pprint(
        CRFAnalyzer().analyze(
            [
                ("The", "DET", None, None),
                ("food", "NOUN", None, None),
                ("is", "VERB", None, None),
                ("very", "ADV", None, None),
                ("good", "ADJ", None, None),
            ],
            [
                [
                    [
                        "word=The",
                        "word.lower=the",
                        "postag=DET",
                        "word.lemmatize=the",
                        "word.is_frequent_term=False",
                        "word.is_stopword=False",
                        "word.headword=food",
                        "word.headword_pos=NN",
                        "word.suffix=The",
                        "word.prefix=The",
                        "governor_relation=",
                        "dependent_relation=",
                        "BOS",
                        "+2:word.lower=is",
                        "+2:postag=VERB",
                        "+1:word.lower=food",
                        "+1:postag=NOUN",
                    ],
                    [
                        "word=food",
                        "word.lower=food",
                        "postag=NOUN",
                        "word.lemmatize=food",
                        "word.is_frequent_term=True",
                        "word.is_stopword=False",
                        "word.headword=good",
                        "word.headword_pos=JJ",
                        "word.suffix=ood",
                        "word.prefix=foo",
                        "governor_relation=",
                        "dependent_relation=nsubj",
                        "-1:word.lower=the",
                        "-1:postag=DET",
                        "+2:word.lower=very",
                        "+2:postag=ADV",
                        "+1:word.lower=is",
                        "+1:postag=VERB",
                    ],
                    [
                        "word=is",
                        "word.lower=is",
                        "postag=VERB",
                        "word.lemmatize=be",
                        "word.is_frequent_term=False",
                        "word.is_stopword=True",
                        "word.headword=good",
                        "word.headword_pos=JJ",
                        "word.suffix=is",
                        "word.prefix=is",
                        "governor_relation=",
                        "dependent_relation=",
                        "-1:word.lower=food",
                        "-1:postag=NOUN",
                        "+1:word.lower=very",
                        "+1:postag=ADV",
                    ],
                    [
                        "word=very",
                        "word.lower=very",
                        "postag=ADV",
                        "word.lemmatize=very",
                        "word.is_frequent_term=False",
                        "word.is_stopword=True",
                        "word.headword=good",
                        "word.headword_pos=JJ",
                        "word.suffix=ery",
                        "word.prefix=ver",
                        "governor_relation=",
                        "dependent_relation=",
                        "-2:word.lower=food",
                        "-2:postag=NOUN",
                        "-1:word.lower=is",
                        "-1:postag=VERB",
                        "+1:word.lower=good",
                        "+1:postag=ADJ",
                    ],
                    [
                        "word=good",
                        "word.lower=good",
                        "postag=ADJ",
                        "word.lemmatize=good",
                        "word.is_frequent_term=False",
                        "word.is_stopword=False",
                        "word.headword=",
                        "word.headword_pos=",
                        "word.suffix=ood",
                        "word.prefix=goo",
                        "governor_relation=nsubj",
                        "dependent_relation=",
                        "-2:word.lower=is",
                        "-2:postag=VERB",
                        "-1:word.lower=very",
                        "-1:postag=ADV",
                        "EOS",
                    ],
                ]
            ],
        )
    )
