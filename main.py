from nltk.corpus import wordnet as wn
from itertools import groupby


class Node():
    def __init__(self, synset):
        self.synset = synset
        self.children = []

    def hypernyms(self):
        return self.synset.hypernyms()

    def __str__(self, level=0):
        res = "\t" * level
        res += self.synset._name
        res += f" ({str(id(self))})"
        for child in self.children:
            res += '\n' + child.__str__(level + 1)
        return res


def build_graph_from_synset_to_entity(synset, nodes):
    head = Node(synset)
    nodes[head.synset] = head
    dfs(head, nodes)
    return head


def dfs(head, nodes):
    for hypernym in head.hypernyms():
        if hypernym in nodes:
            head.children.append(nodes[hypernym])
        else:
            node = Node(hypernym)
            head.children.append(node)
            nodes[node.synset] = node
            dfs(node, nodes)


def get_top_synstets(words, pos=wn.NOUN):
    synsets = [synset for word in words for synset in wn.synsets(word, pos)]
    nodes = {}
    leaves = [build_graph_from_synset_to_entity(
        synset, nodes) for synset in synsets]


get_top_synstets(['cat', 'dog'])
