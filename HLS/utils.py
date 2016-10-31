"""
    Utility module for results

    Author: Jake Poirier
    Date: 8/12/16
"""
import math


def median(scores):
    """
    Computes median of a list of scores
    :param scores: list of scores
    :return: median of that list
    """
    if len(scores) == 0:
        return 0
    scores = sorted(scores)
    return scores[((len(scores)+1) / 2) - 1]


def std_deviation(scores, mean):
    """
    Computes std deviation of a list of scores
    :param scores: list of scores
    :param mean: median of that list
    :return: stnd deviation of the list
    """
    if len(scores) == 0:
        return 0
    numerator = math.fsum([math.pow(score - mean, 2) for score in scores])
    denominator = len(scores)
    return round(math.sqrt((numerator/denominator)), 2)


def average(scores):
    """
    Computes average/mean of list
    :param scores: list of scores
    :return: mean of list
    """
    sum = 0
    if len(scores) == 0:
        return 0
    for score in scores:
        sum += score
    return sum / len(scores)
