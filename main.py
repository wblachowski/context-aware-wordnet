from nltk.corpus import wordnet as wn


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
            for hypernym in head.hypernyms():
                node = Node(hypernym)
                node.children.append(head)
                new_heads.extend(dfs([node]))
        else:
            new_heads.append(head)
    return new_heads


def get_top_synstets(words, pos=wn.NOUN):
    synsets = [wn.synsets(word, pos) for word in words]
    dog = synsets[1][0]
    paths = build_paths_from_entity_to_synset(dog)


get_top_synstets(['cat', 'dog'])
