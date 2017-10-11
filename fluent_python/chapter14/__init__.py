# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

import reprlib
from collections import Iterable


class Sentence:
    
    def __init__(self, text):
        self.text = text
        self.words = re.compile("\w+").findall(text)
    
    # def __getitem__(self, item):
    #     print '__getitem__'
    #     if isinstance(item, int):
    #         return self.words[item]
    #     elif isinstance(item, slice):
    #         return self.words[item]
    #     else:
    #         raise ValueError("item error")

    def gen(self):
        print '__iter__'
        return (one for one in self.words)
            # yield one

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return "Sentence(%s)" % reprlib.repr(self.text)


class SentenceIterator:
    def __init__(self, words):
        self.index = 0
        self.words = words

    # def __getitem__(self, item):
    #     print '__getitem__'
    #     if isinstance(item, int):
    #         return self.words[item]
    #     elif isinstance(item, slice):
    #         return self.words[item]
    #     else:
    #         raise ValueError("item error")
    def next(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self



