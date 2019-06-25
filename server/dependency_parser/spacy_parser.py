import spacy
import json
import sys
import string
from pprint import pprint


class SpacyParser:
    def __init__(self):
        self.nlp = spacy.load("en")
        self.result = list()
        print("Spacy Parser instantiated")

    def parse(self, sentence):
        document = self.nlp(sentence)
        edges = list()
        # edges = [token.orth_ for token in document if not token.is_punct]

        for token in document:
            # FYI https://spacy.io/docs/api/token

            for child in token.children:
                edges.append(
                    (
                        "{0}-{1}".format(token.lower_, token.i),
                        "{0}-{1}".format(child.lower_, child.i),
                    )
                )

        return edges


if __name__ == "__main__":
    parser = SpacyParser()
    pprint(parser.parse("The food is very good."))
