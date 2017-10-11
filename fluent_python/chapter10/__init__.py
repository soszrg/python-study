# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class SelfList(object):

    def __init__(self, base):
        self._base = base

    # def __iter__(self):
    #     return iter(self._base)

    def __getitem__(self, item):
        return self._base[item]

    # def __len__(self):
    #     return len(self._base)