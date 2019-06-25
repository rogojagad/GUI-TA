from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from pprint import pprint


class SentiWordNetValueGetter:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

        print("SentiWordNet Lexicon Value Getter instantiated...")

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

    def get_value(self, token):
        sentiment = 0.0
        token_counts = 0
        word = token[0]
        pos_tag = token[1]

        wn_tag = self.penn_to_wn(pos_tag)

        if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV, wn.VERB):
            return 0

        lemma = self.lemmatizer.lemmatize(word, pos=wn_tag)

        if not lemma:
            return 0

        return self.analyze_value(lemma, wn_tag)

    def analyze_value(self, word, tag):
        synsets = wn.synsets(word, pos=tag)

        if not synsets:
            return 0

        swn_synset = swn.senti_synset(synsets[0].name())

        pos_score = swn_synset.pos_score()
        neg_score = swn_synset.neg_score()
        obj_score = swn_synset.obj_score()

        if pos_score > neg_score and pos_score >= obj_score:
            return pos_score
        elif neg_score > pos_score and neg_score >= obj_score:
            return neg_score * -1
        else:
            return 0

        # return pos_score - neg_score


if __name__ == "__main__":
    pass
    # Do class testing here

    getter = SentiWordNetValueGetter()

    print(getter.get_value(("stale", "ADJ", "O")))
