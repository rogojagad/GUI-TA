import json
from .base_value_getter import BaseValueGetter


class MPQALexiconValueGetter(BaseValueGetter):
    def __init__(self):
        with open(self.data_dir + "mpqa_lexicon\lexicon.json") as f:
            self.lexicon = json.load(f)

        print("MPQA Lexicon Value Getter instantiated...")

    def get_value(self, word):
        try:
            subjectivity = self.lexicon[word]["subjectivity"]
            polarity = self.lexicon[word]["polarity"]

            if subjectivity == "strongsubj":
                if polarity == "positive":
                    return 1
                elif polarity == "negative":
                    return -1
                else:
                    return 0
            elif subjectivity == "weaksubj":
                if polarity == "positive":
                    return 0.5
                elif polarity == "negative":
                    return -0.5
                else:
                    return 0

        except KeyError:
            return 0


if __name__ == "__main__":
    getter = MPQALexiconValueGetter()

    print(getter.get_value("however"))
