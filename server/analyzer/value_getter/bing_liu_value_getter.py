import pickle
from .base_value_getter import BaseValueGetter


class BingLiuLexiconValueGetter(BaseValueGetter):
    def __init__(self):
        with open(
            self.data_dir + "/bing-liu-opinion-lexicon/positive-words.pickle", "rb"
        ) as inp:
            self.positive_lex = pickle.load(inp)

        with open(
            self.data_dir + "/bing-liu-opinion-lexicon/negative-words.pickle", "rb"
        ) as inp:
            self.negative_lex = pickle.load(inp)

        print("Bing Liu Value Getter instantiated...")

    def get_value(self, token):
        if token in self.positive_lex:
            return 1
        elif token in self.negative_lex:
            return -1
        else:
            return 0


if __name__ == "__main__":
    getter = BingLiuLexiconValueGetter()

    print(getter.get_value("cool"))
