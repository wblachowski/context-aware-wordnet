from nltk.corpus import wordnet as wn


def get_top_synstets(words, pos=wn.NOUN):
    synsets = [wn.synsets(word, pos) for word in words]
    print(synsets)


get_top_synstets(['cat', 'dog'])
