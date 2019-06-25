import networkx as nx
import pickle
from pprint import pprint
from spacy import displacy


class DependencyPathDistanceGetter:
    def __init__(self, inp):
        self.edges_list = inp

        print("Dependency Path Distance Getter instantiated...")

    def get_distance_value(self, source, source_idx, target, target_idx):
        """
        Parameters: source token, source token index, target token, target token index, sentence index
        """

        graph = nx.Graph(self.edges_list)

        source += "-" + str(source_idx)
        target += "-" + str(target_idx)

        try:
            return nx.shortest_path_length(graph, source=source, target=target)
        except nx.exception.NetworkXNoPath:
            return 1
        except nx.exception.NodeNotFound:
            return 1


if __name__ == "__main__":
    # getter = DependencyPathDistanceGetter()

    # print(getter.get_distance_value("amazing", 3, "service", 4, 100))
    # # pprint(getter.edges_list[100])
    pass
