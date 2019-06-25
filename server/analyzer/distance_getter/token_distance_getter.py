from pprint import pprint


class TokenDistanceGetter:
    def __init__(self):
        self.list_of_word = []
        self.aspect_words_list = []

        print("Token Distance Getter instantiated...")

    def set_sentence(self, list_of_token):
        self.aspect_words_list = list()
        self.list_of_word = self.merge_aspect_term(list_of_token)

    def get_distance_value(self, aspect_term, target_idx, opinion_word, opinion_idx):
        # target_idx = self.list_of_word.index(aspect_term)
        # opinion_idx = self.list_of_word.index(opinion_word)
        value = abs(opinion_idx - target_idx) - 1
        if value == 0:
            return 1
        else:
            return value

    def merge_aspect_term(self, list_of_token):
        words = []

        for i in range(len(list_of_token)):
            if list_of_token[i][2] == "O":
                words.append(list_of_token[i][0])
            elif list_of_token[i][2] == "B":
                temp = list_of_token[i][0]

                for j in range(i + 1, len(list_of_token)):
                    if list_of_token[j][2] == "I":
                        temp += " " + list_of_token[j][0]
                    else:
                        break

                words.append(temp)
                self.aspect_words_list.append(temp)

        return words


if __name__ == "__main__":
    getter = TokenDistanceGetter()

    getter.set_sentence(
        [
            ("When", "WRB", "O"),
            ("the", "DT", "O"),
            ("main", "JJ", "B"),
            ("course", "NN", "I"),
            ("finally", "RB", "O"),
            ("arrived", "VBD", "O"),
            ("another", "DT", "O"),
            ("mins", "NNS", "O"),
            ("half", "NN", "O"),
            ("of", "IN", "O"),
            ("our", "PRP$", "O"),
            ("order", "NN", "O"),
            ("was", "VBD", "O"),
            ("missing", "VBG", "O"),
        ]
    )

    print(getter.get_distance_value("main course", "missing"))
