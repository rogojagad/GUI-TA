import json
import os
import sys
from pprint import pprint

from nltk.parse import stanford


class StandfordDependencyParser:
    def __init__(self):
        os.environ["JAVAHOME"] = "C:\Program Files\Java\jdk1.8.0_151\\bin"

        jar_path = "D:\Stanford Core NLP\stanford-corenlp-full-2018-10-05\stanford-corenlp-3.9.2.jar"
        model_path = "D:\Stanford Core NLP\stanford-corenlp-full-2018-10-05\stanford-corenlp-3.9.2-models.jar"

        self.parser = stanford.StanfordDependencyParser(
            path_to_jar=jar_path, path_to_models_jar=model_path
        )

        print("Standford Dependency Parser instantiated")

    def parse(self, sentence):
        sentences = self.parser.raw_parse(sentence)

        dep = sentences.__next__()
        parsed = list(dep.triples())

        return parsed

    def get_governor_relation(self, tokenized, results):
        needed_relation = ["amod", "nsubj", "dep"]
        rel = {}

        for token in tokenized:
            for data in results:
                if data[0][0] == token and data[1] in needed_relation:
                    if token in rel:
                        if data[1] not in rel[token].split(";"):
                            rel[token] += ";" + data[1]
                    else:
                        rel[token] = data[1]

        return rel

    def get_dependent_relation(self, tokenized, results):
        rel = {}
        needed_relation = ["dobj", "nsubj", "dep"]

        for token in tokenized:
            for data in results:
                if data[2][0] == token and data[1] in needed_relation:
                    if token in rel:
                        if data[1] not in rel[token].split(";"):
                            rel[token] += ";" + data[1]
                    else:
                        rel[token] = data[1]

        return rel


# if __name__ == "__main__":
#     parser = StandfordDependencyParser()

#     pprint(parser.parse("The food is very good."))
