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


def calculate_score(head):
    def dfs(head, acc):
        acc.append(head)
        for child in head.children:
            dfs(child, acc)
    path = []
    dfs(head, path)
    return sum([n.support for n in path])/len(path)


def get_top_synstets(words, pos=wn.NOUN):
    result = []
    synsets = [wn.synsets(word, pos) for word in words]
    for i, word_synsets in enumerate(synsets):
        other_synsets = synsets[:i]+synsets[i+1:]
        other_synsets = [s for syn in other_synsets for s in syn]
        synset_scores = []
        for word_synset in word_synsets:
            nodes = {}
            [build_graph_from_synset_to_entity(
                synset, nodes) for synset in other_synsets]
            leaf = build_graph_from_synset_to_entity(word_synset, nodes)
            score = calculate_score(leaf)
            synset_scores.append((leaf.synset, score))
        best_synset = sorted(
            synset_scores, key=lambda x: x[1], reverse=True)[0][0]
        result.append(best_synset)
    return result


words = ['pig', 'dog', 'gun', 'children']
for word, synset in zip(words, get_top_synstets(words)):
    print(f"{word}:")
    print(f"\t{synset.definition()}")
