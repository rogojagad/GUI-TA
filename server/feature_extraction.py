import pickle
import sys
from pprint import pprint
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn


class FeatureExtractor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

        with open(
            "D:\Kuliah\TA With UI\server\data\\frequent_term.pickle", "rb"
        ) as inp:
            self.frequent_term = pickle.load(inp)

        self.stopwords = stopwords.words("english")

        print("Feature Extractor instantiated")

    def penn_to_wn(self, tag):
        if tag.startswith("ADJ"):
            return wn.ADJ
        elif tag.startswith("NOUN"):
            return wn.NOUN
        elif tag.startswith("ADV"):
            return wn.ADV
        elif tag.startswith("VERB"):
            return wn.VERB

        return None

    def word2features(self, doc, token_headword_data, i):
        word = doc[i][0]
        postag = doc[i][1]
        # pprint(doc)
        if not token_headword_data[1]:
            token_headword = ""
        else:
            token_headword = token_headword_data[1]

        if not token_headword_data[2]:
            headword_pos = ""
        else:
            headword_pos = token_headword_data[2]

        governor_relation = ""
        dependent_relation = ""
        wn_postag = self.penn_to_wn(postag)

        if wn_postag == None:
            lemmatized = self.lemmatizer.lemmatize(word.lower())
        else:
            lemmatized = self.lemmatizer.lemmatize(word.lower(), wn_postag)

        if doc[i][2] != None:
            governor_relation = doc[i][2]

        if doc[i][3] != None:
            dependent_relation = doc[i][3]

        if word in self.frequent_term:
            frequent = True
        else:
            frequent = False

        if word in self.stopwords:
            is_stopword = True
        else:
            is_stopword = False

        # Common features for all words
        features = [
            "word=" + word,
            "word.lower=" + word.lower(),
            "postag=" + postag,
            "word.lemmatize=" + lemmatized,
            "word.is_frequent_term=%s" % frequent,
            "word.is_stopword=%s" % is_stopword,
            "word.headword=" + token_headword,
            "word.headword_pos=" + headword_pos,
            "word.suffix=" + word[-3:],
            "word.prefix=" + word[0:3],
            "governor_relation=" + governor_relation,
            "dependent_relation=" + dependent_relation,
        ]

        if i - 2 > 0:
            word1 = doc[i - 2][0]
            postag1 = doc[i - 2][1]
            features.extend(["-2:word.lower=" + word1.lower(), "-2:postag=" + postag1])

        # Features for words that are not
        # at the beginning of a document
        if i > 0:
            word1 = doc[i - 1][0]
            postag1 = doc[i - 1][1]
            features.extend(["-1:word.lower=" + word1.lower(), "-1:postag=" + postag1])
        else:
            # Indicate that it is the 'beginning of a document'
            features.append("BOS")

        if i + 2 < len(doc) - 1:
            word1 = doc[i + 2][0]
            postag1 = doc[i + 2][1]
            features.extend(["+2:word.lower=" + word1.lower(), "+2:postag=" + postag1])

        # Features for words that are not
        # at the end of a document
        if i < len(doc) - 1:
            word1 = doc[i + 1][0]
            postag1 = doc[i + 1][1]
            features.extend(["+1:word.lower=" + word1.lower(), "+1:postag=" + postag1])
        else:
            # Indicate that it is the 'end of a document'
            features.append("EOS")

        return features

    def extract_features(self, doc, headword_data):
        return [self.word2features(doc, headword_data[i], i) for i in range(len(doc))]


if __name__ == "__main__":
    extractor = FeatureExtractor()

    data = [
        ("The", "DET", None, None),
        ("food", "NOUN", None, "nsubj"),
        ("is", "VERB", None, None),
        ("very", "ADV", None, None),
        ("good", "ADJ", "nsubj", None),
    ]

    headword = [
        ("The", "food", "NN"),
        ("food", "good", "JJ"),
        ("is", "good", "JJ"),
        ("very", "good", "JJ"),
        ("good", None, None),
    ]

    X = [extractor.extract_features(data, headword)]
    #     y = [extract_labels(doc) for doc in docs]

    pprint(X)

#     export(X, "\\test\\features.pickle")
#     export(y, "\\test\\labels.pickle")

