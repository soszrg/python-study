# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def twoSum(nums, target):
    ordered_nums = sorted(nums)
    if ordered_nums[0] > target:
        return False

    for i in range(len(ordered_nums)):
        if ordered_nums[i] > target:
            return False
