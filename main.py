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
        for child in self.children:
            res += '\n' + child.__str__(level + 1)
        return res


def build_paths_from_entity_to_synset(synset):
    heads = dfs([Node(synset)])
    return heads


def dfs(heads):
    new_heads = []
    for head in heads:
        hypernyms = head.hypernyms()
        if len(hypernyms):
            for hypernym in hypernyms:
                node = Node(hypernym)
                node.children.append(head)
                new_heads.extend(dfs([node]))
        else:
            new_heads.append(head)
    return new_heads


def merge_paths(head):
    def key(n): return n.synset
    new_head = Node(head.synset)
    grouped = groupby(sorted(head.children, key=key), key=key)
    nodes = []
    for key, group in grouped:
        group = list(group)
        node = Node(group[0].synset)
        for el in group:
            node.children.extend(el.children)
        nodes.append(node)
    for node in nodes:
        new_head.children.append(merge_paths(node))
    return new_head


def get_top_synstets(words, pos=wn.NOUN):
    synsets = [synset for word in words for synset in wn.synsets(word, pos)]
    paths = [
        path for synset in synsets for path in build_paths_from_entity_to_synset(synset)]
    for path in paths:
        print(path)
    head = Node(paths[0].synset)
    for path in paths:
        head.children.extend(path.children)
    new_head = merge_paths(head)
    print(new_head)


get_top_synstets(['cat', 'dog'])
