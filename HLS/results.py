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
            print result
            scores.append(result.score)
        print scores
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


def results_process_questions(quizjson):
    question_index = 0
    overall_dict = []
    for answer in quizjson['answers']:
        choice_a = answer['choices'][0]
        choice_b = answer['choices'][1]
        choice_c = answer['choices'][2]
        choice_d = answer['choices'][3]
        if answer['correct'] == choice_a:
            correct = 'buttonA'
        elif answer['correct'] == choice_b:
            correct = 'buttonB'
        elif answer['correct'] == choice_c:
            correct = 'buttonC'
        else:
            correct = 'buttonD'

        temp = {'question': question_index,
                'question_name': quizjson['questions'][question_index],
                'correct': correct}
        overall_dict.append(temp)
        question_index += 1
    return overall_dict


def results_process_data(post_dict, overall_dict, devices):
    results_dict = []
    for key, value in post_dict.iteritems():
        if 'question' in key:
            for device in devices:
                if str(device.id) in json.loads(post_dict[key]).keys():
                    value_dict = json.loads(post_dict[key])[str(device.id)]
                    question_num = key[-1]

                    answer = overall_dict[int(question_num)]['correct']
                    score = {'question': question_num,
                             'question_name': overall_dict[int(question_num)]['question_name'],
                             'score': value_dict[answer],
                             'student': device.student.name}
                    results_dict.append(score)
    return results_dict