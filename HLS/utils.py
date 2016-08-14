"""
    Helper functions to do quick calculations for pages
"""
import math


def median(scores):
    """
    Find the median of a list by sorting then taking middle value
    :param scores: incoming list of scores
    :return: median of that list
    """
    scores = sorted(scores)
    return scores[((len(scores)+1) / 2) - 1]


def std_deviation(scores, mean):
    """
    Find the standard deviation of a list
    :param scores: incoming list of scores
    :param mean: the mean of the list
    :return: std dev
    """
    numerator = math.fsum([math.pow(score - mean, 2) for score in scores])
    denominator = len(scores)
    if denominator == 0:
        return 0
    return round(math.sqrt((numerator/denominator)), 2)


def average(scores):
    """
    Find the average of a list
    :param scores: incoming list of scores
    :return: average
    """
    sum = 0
    for score in scores:
        sum += score
    if len(scores) == 0: return 0
    return sum / len(scores)
