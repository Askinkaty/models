# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager, NamespaceProxy

unknown_label = 'UNKNOWN'
padding_label = 'PADDING'
number_label = 'NUMBER'
name_label = 'NAME'
punct_label = 'PUNCT'

def merge_words(lemma, pos, prop):
    if pos == 'Num':
        return number_label
    elif pos == 'Punct':
        return punct_label
    elif prop:
        return name_label
    else:
        return lemma

class Vocab():
    def __init__(self, special_labels=False):
        self.word2index = {}
        self.index2word = {}
        self.index = 0
        if special_labels:
            self.add(padding_label)
            self.add(unknown_label)
            self.add(number_label)
            self.add(name_label)
    def add(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.index
            self.index2word[self.index] = word
            self.index += 1
            return self.index - 1
        else:
            return self.word2index[word]
    def save(self, output_file):
        with open(output_file, 'w') as f:
            for i in range(self.index):
                try:
                    print(self.index2word[i], file=f)
                # Just in case there's a missing key
                except KeyError:
                    continue
    @staticmethod
    def load(input_file):
        vocab = Vocab()
        with open(input_file, 'r') as f:
            for word in f:
                vocab.add(word.strip())
        return vocab
    def __getitem__(self, key):
        t = type(key)
        try:
            if t == str:
                return self.word2index[key]
            elif t == int:
                return self.index2word[key]
            else:
                raise KeyError(key)
        except KeyError:
            return self.word2index[unknown_label]
    def __len__(self):
        return self.index
    def __repr__(self):
        return ''.join(
            f'{i} -> {self.index2word[i]}'
            for i in range(self.index)
        )

class VocabManager(BaseManager):
    pass

class VocabProxy(NamespaceProxy):
    _exposed_ = (
        '__getattribute__',
        '__setattr__',
        '__delattr__',
        '__getitem__',
        '__len__',
        'add',
        'save'
    )
    def add(self, word):
        return self._callmethod('add', [word])
    def save(self, output_file):
        return self._callmethod('save', [output_file])

VocabManager.register('Vocab', Vocab, VocabProxy)
