"""
    Results aggregator module which compiles all results for
    each student. Shows all data on results page on app

    Author: Jake Poirier
    Date: 8/12/16
"""

from models import Quiz, Results, Device, Student
import xlsxwriter
import utils
import json
import datetime
from django.shortcuts import HttpResponse, render


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
    """
    Helper method to get index of number of
    question in results to the number correct in
    the quiz dict
    :param quizjson:
    :return:
    """
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
    """
    Helper method to cross reference data in results from
    javascript to the data in the database for correct
    answers in a quiz
    :param post_dict: request.POST dict
    :param overall_dict: dict with corresponding button names
    :param devices: all devices in database table
    :return: dict with all scores
    """
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


def result_post_method(request):
    """
    Point to post data from quiz into results
    table in dictionary. Comes in as (sample of 3 mats, 1 question):
    <QueryDict: {
        u'overall': [u'{
            "A": 0,
            "node_data": {
                "1001": {
                    "buttonC": "0",
                    "buttonB": "0",
                    "buttonA": "1",
                    "buttonD": "0"
                },
                "1002": {
                    "buttonC": "0",
                    "buttonB": "0",
                    "buttonA": "0",
                    "buttonD": "1"
                },
                "1003": {
                    "buttonC": "0",
                    "buttonB": "1",
                    "buttonA": "0",
                    "buttonD": "0"
                }
            },
            "B": 2,
            "C": 3,
            "D": 8
        }'],
        u'question0': [u'{
            "1001": {
                "buttonC": "0",
                "buttonB": "0",
                "buttonA": "1",
                "buttonD": "0"
            },
            "1002": {
                "buttonC": "0",
                "buttonB": "0",
                "buttonA": "0",
                "buttonD": "1"
            },
            "1003": {
                "buttonC": "0",
                "buttonB": "1",
                "buttonA": "0",
                "buttonD": "0"
            }
        }']
    }>

    Then processes the data into manageable pieces
    to be cross referenced with the correct answers
    in the quiz dictionaries. The device ids that are
    attached to each mat are also cross referenced to
    whatever student is linked to that device, and
    given a score in results.
    :param request: wsgi request
    :return: HTTP response
    """
    quizname = request.GET.get('quizname')
    devices = Device.objects.all()
    quiz_obj = Quiz.objects.get(name=quizname)

    quizjson = json.loads(quiz_obj.quizjson)
    overall_dict = results_process_questions(quizjson)

    post_dict = request.POST
    results_dict = results_process_data(post_dict, overall_dict, devices)

    for device in devices:
        score = 0
        for result in results_dict:
            if device.student.name in result['student']:
                score += int(result['score'])
        try:
            result = Results()
            result.quiz = quiz_obj
            result.student = device.student
            result.score = score
            result.save()
        except Exception:
            return HttpResponse("failure")

    return HttpResponse("success")


def xlsx_handler(request):
    """
    Method to write data from results into
    spread sheet or xlsx. Takes all data from
    student, quiz, results and device tables and
    aggregates it into a column on the xlsx. Stores a
    most recent results spreadsheet as a temporary
    store before the client can download it. This
    allows the system to have a backup of the last
    results saved.

    Writes the file name as:
        Results-DATE.xlsx

    Common error: running in def env, the dir
        must be changed ex. on windows
    :param request: wsgi request
    :return: render method for either an error or file response
    """
    results = Results.objects.all()
    students = Student.objects.all()
    quizzes = Quiz.objects.all()
    devices = Device.objects.all().order_by('student__name')
    try:
        workbook = xlsxwriter.Workbook("Results.xlsx")
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        worksheet.write('B1', 'Student', bold)
        worksheet.write('C1', 'Student_ID', bold)
        worksheet.write('D1', 'Device_ID', bold)
        for quiz in quizzes:
            worksheet.write(0, quiz.id + 3, quiz.name, bold)

        for index in range(len(devices)):
            worksheet.write(index + 1, 1, devices[index].student.name)
            worksheet.write(index + 1, 2, devices[index].student.id)
            worksheet.write(index + 1, 3, devices[index].id)
            for result in results:
                for quiz in quizzes:
                    if devices[index].student.name == result.student.name and result.quiz.name == quiz.name:
                        worksheet.write(index + 1, quiz.id + 3, result.score)

        workbook.close()

        raw_text = open("/home/pi/HoppoRoo/HoppoRoo/Results.xlsx", 'rb').read()

        response = HttpResponse(raw_text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            "Results" + str(datetime.datetime.now().date()) + ".xlsx")

        return response
    except Exception:
        error_message = '''Failure to write to worksheet/spreadsheet. Please ensure that the spreadsheet
                            for today has been closed.'''
        return render(request, 'generic_error.html', {"error_message": error_message,
                                                      "return": '/results'})
