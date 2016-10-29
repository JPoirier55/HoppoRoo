"""
    Results aggregator module which compiles all results for
    each student. Shows all data on results page on app

    Author: Jake Poirier
    Date: 8/12/16
"""

from models import Quiz, Results
import utils
import json


def results_metrics():
    """
    Aggregator for all student results data
    :return: dictionary for all student data
    """
    quizzes = Quiz.objects.all()
    metrics = {}
    for quiz in quizzes:
        results = Results.objects.filter(quiz=quiz)
        quiz_json = json.loads(quiz.quizjson)
        scores = []
        single_metrics = {}
        for result in results:
            scores.append(result.score)
        single_metrics['scores'] = scores
        single_metrics['name'] = quiz.name
        single_metrics['num_of_questions'] = len(quiz_json['questions'])
        mean = utils.average(scores)
        single_metrics['class_av'] = mean
        single_metrics['std_dev'] = utils.std_deviation(scores, mean)
        single_metrics['subject'] = quiz.subject
        single_metrics['high'] = max(scores)
        single_metrics['low'] = min(scores)
        single_metrics['class_median'] = utils.median(scores)
        metrics[quiz.name] = single_metrics
    return metrics
