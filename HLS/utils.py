import requests
import json
import math


def median(scores):
    scores = sorted(scores)
    return scores[((len(scores)+1) / 2) - 1]


def std_deviation(scores, mean):
    numerator = math.fsum([math.pow(score - mean, 2) for score in scores])
    denominator = len(scores)
    return round(math.sqrt((numerator/denominator)), 2)


def average(scores):
    sum = 0
    for score in scores:
        sum += score
    return sum / len(scores)
