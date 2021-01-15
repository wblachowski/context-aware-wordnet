from nltk.corpus import wordnet as wn


class Tree():
    def __init__(self):
        self.is_empty = True


class Node():
    def __init__(self, synset):
        self.synset = synset
        self.children = []


def build_tree_from_synset_to_entity(synset):
    head = Node(synset)
    dfs(head)
    return head


def dfs(head):
    for hypernym in head.synset.hypernyms():
        head.children.append(Node(hypernym))
    for child in head.children:
        dfs(child)


def get_top_synstets(words, pos=wn.NOUN):
    synsets = [wn.synsets(word, pos) for word in words]
    dog = synsets[1][0]
    head = build_tree_from_synset_to_entity(dog)
    print(head.synset)


get_top_synstets(['cat', 'dog'])
