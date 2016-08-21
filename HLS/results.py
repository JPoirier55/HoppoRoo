"""
    Module to produce metrics for results page, uses utils methods

"""

from models import Quiz, Results
import utils
import json


def results_metrics(quizzes):
    """
    Builds dict of values for each quiz which gets passed
    to render the page and tables
    :return: dict of metrics
    """
    quizzes = Quiz.objects.all()
    metrics = {}

    for quiz in quizzes:
        results = Results.objects.filter(quiz=quiz)
        if not results:
            break
        quiz_json = json.loads(quiz.quizjson)
        single_metrics = {}
        scores = [float(result.score) for result in results]
        single_metrics['scores'] = scores
        single_metrics['name'] = quiz.name
        single_metrics['num_of_questions'] = len(quiz_json)
        mean = utils.average(scores)
        single_metrics['class_av'] = mean
        single_metrics['std_dev'] = utils.std_deviation(scores, mean)
        single_metrics['subject'] = quiz.subject
        single_metrics['high'] = max(scores)
        single_metrics['low'] = min(scores)
        single_metrics['class_median'] = utils.median(scores)
        metrics[quiz.name] = single_metrics
    return metrics


def build_chart(request, metrics):
    quiz = request.GET.get('quiz')
    if not quiz:
        return None
    else:
        highchart_json = '''{
                    global: {
                        useUTC: false
                    },
                    plotOptions: {
                        column: {
                            colorByPoint: true
                        }
                    },
                    colors: [
                        '#932933',
                        '#00ED77',
                        '#2E3B7F',
                        '#FCF528'
                    ]
                }'''