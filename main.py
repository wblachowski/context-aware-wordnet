from nltk.corpus import wordnet as wn


class Tree():
    def __init__(self):
        self.is_empty = True


class Node():
    def __init__(self, synset):
        self.synset = synset
        self.children = []

    def __str__(self, level=0):
        res = "\t" * level
        res += self.synset._name
        for child in self.children:
            res += '\n' + child.__str__(level + 1)
        return res


def build_tree_from_synset_to_entity(synset):
    heads = dfs([Node(synset)])
    print(heads[0])
    return heads


def dfs(heads):
    new_heads = []
    for head in heads:
        can_extend = False
        for hypernym in head.synset.hypernyms():
            can_extend = True
            node = Node(hypernym)
            node.children.append(head)
            new_heads.extend(dfs([node]))
        if not can_extend:
            new_heads.append(head)
    return new_heads


def get_top_synstets(words, pos=wn.NOUN):
    synsets = [wn.synsets(word, pos) for word in words]
    dog = synsets[1][0]
    heads = build_tree_from_synset_to_entity(dog)


get_top_synstets(['cat', 'dog'])
