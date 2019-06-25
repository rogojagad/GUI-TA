from preprocess import Preprocessor
from feature_extraction import FeatureExtractor
from analyzer.crf_analyzer import CRFAnalyzer
from analyzer.sentiment_analyzer import SentimentAnalyzer
from pprint import pprint


class ProcessController:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.feature_extractor = FeatureExtractor()
        self.crf_analyzer = CRFAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()

        print("\nAll module instantiated and ready to go....\n")

    def start_process(self, sentence):
        data = dict()

        preprocess_result, headword_data, spacy_parsing_result = self.preprocessor.start_preprocess(
            sentence
        )

        features = [
            self.feature_extractor.extract_features(preprocess_result, headword_data)
        ]

        crf_result = self.crf_analyzer.analyze(preprocess_result, features)

        self.sentiment_analyzer.create_graph_data(spacy_parsing_result)

        sentiment_analyzer_result = self.sentiment_analyzer.analyze(crf_result)

        data["sentence"] = sentence
        data["result"] = sentiment_analyzer_result

        return data


if __name__ == "__main__":
    pprint(ProcessController().start_process("The food is very good."))
