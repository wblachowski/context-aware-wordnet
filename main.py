from nltk.corpus import wordnet as wn
from itertools import groupby


class Node():
    def __init__(self, synset, support=1):
        self.synset = synset
        self.support = support
        self.children = []

    def hypernyms(self):
        return self.synset.hypernyms()

    def __str__(self, level=0):
        res = "\t" * level
        res += self.synset._name
        res += f" {self.support}"
        res += f" ({str(id(self))})"
        for child in self.children:
            res += '\n' + child.__str__(level + 1)
        return res


def build_graph_from_synset_to_entity(synset, nodes):
    head = Node(synset)
    nodes[head.synset] = head
    dfs(head, nodes, head.support)
    return head


def dfs(head, nodes, val):
    hypernyms = head.hypernyms()
    for hypernym in hypernyms:
        if hypernym in nodes:
            node = nodes[hypernym]
            value = val/len(hypernyms)
            node.support += value
            dfs(node, nodes, value)
            if node not in head.children:
                head.children.append(node)
        else:
            node = Node(hypernym, val/len(hypernyms))
            head.children.append(node)
            nodes[node.synset] = node
            dfs(node, nodes, node.support)


def get_top_synstets(words, pos=wn.NOUN):
    synsets = [
        synset for word in words for synset in wn.synsets(word, pos)]
    nodes = {}
    leaves = [build_graph_from_synset_to_entity(
        synset, nodes) for synset in synsets]
    print(leaves[0])


get_top_synstets(['car'])
