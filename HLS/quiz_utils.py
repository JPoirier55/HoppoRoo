import requests
import json
import os
from models import Quiz, PDFQuiz
from django.shortcuts import HttpResponse, HttpResponseRedirect
import datetime


def pdf_builder():
    """
    Util method to fetch all pdfs on file
    :return: list of pdfs at dir
    """
    pdfs = []
    dir = '/home/pi/HoppoRoo/HoppoRoo/static/res/'
    # dir = 'C:\\Users\\Jake\\git3\\HoppoRoo\\static\\res\\'
    for pdf in os.listdir(dir):
        if 'pdf' in pdf:
            pdf = {'name': pdf,
                   'dir': dir+pdf}
            pdfs.append(pdf)
    return pdfs


def question_builder(request):
    """
    Util method to aggregate all data for
    quiz to be shown in quiz question view
    :param request: wsgi request
    :return: dict with all quiz data
    """
    selected_quiz = request.GET.get('quizname', '')
    question_num = request.GET.get('question_num', 0)
    show_correct = request.GET.get('show_correct', 'false')
    quiz = Quiz.objects.get(name=selected_quiz)
    quizjson = json.loads(quiz.quizjson)
    question = quizjson['questions'][int(question_num)]
    choice_a = quizjson['answers'][int(question_num)]['choices'][0]
    choice_b = quizjson['answers'][int(question_num)]['choices'][1]
    choice_c = quizjson['answers'][int(question_num)]['choices'][2]
    choice_d = quizjson['answers'][int(question_num)]['choices'][3]
    return {'quizname': selected_quiz,
            'question_num': question_num,
            'show_correct': show_correct,
            'question': question,
            'choice_a': choice_a,
            'choice_b': choice_b,
            'choice_c': choice_c,
            'choice_d': choice_d}


def quiz_loader(request):
    """
    Util method to aggregate all quizzes to see
     recent ones in the quiz archive section
    :param request: wsgi request
    :return: dict of quizzes data
    """
    id = request.GET.get('id')
    quiz_names = []
    quiz_ids = []
    qt = []
    quizzes = Quiz.objects.all()
    for quiz in quizzes:
        quiz_names.append(quiz.name)
        quiz_ids.append(quiz.id)
        qt.append(quiz)
    if id is None:
        quiz_obj = {}
    else:
        quiz_obj = json.loads(Quiz.objects.get(id=id).quizjson)

    return {'chosen_quiz': quiz_obj,
            'quiz_ids': quiz_ids,
            'quiz_names': quiz_names,
            'qt': qt}


def build_quiz_api():
    """
    Deprecated helper method returns
    json of quizzes that can be pulled
    from the database
    :return: HTTP response with json data
    """
    quizzes = Quiz.objects.all()
    quiz_json = []
    for quiz in quizzes:
        quiz_json.append(quiz.quizjson)
    return HttpResponse(json.dumps(quiz_json))


def create_quiz_method(request):
    """
    Method which builds a quiz from the quiz creator page.
    This takes all data from the final results form and
    injects it into the Quiz and/or PDFquiz tables
    :param request: wsgi request
    :return: Redirect response after buidling table
    """
    post_dict = request.POST
    get_dict = request.GET

    question_count = 0
    quiz_model = None
    questions = []
    question_elements = []

    for key, value in post_dict.iteritems():
        if 'question' in key:
            question_count += 1

    if get_dict['pdf'] == 'true':
        for i in range(question_count):
            index = str(i)
            quiz_model = PDFQuiz()
            questions.append(post_dict['question' + index])
            temp_dict = {'question_num': index,
                         'correct': post_dict['question' + index]}
            question_elements.append(temp_dict)
    else:
        for i in range(question_count):
            index = str(i)
            quiz_model = Quiz()
            questions.append(post_dict['question' + index])
            temp_dict = {'correct': post_dict['correct' + index],
                         'choices': [post_dict['choice1' + index],
                                     post_dict['choice2' + index],
                                     post_dict['choice3' + index],
                                     post_dict['choice4' + index]]}
            question_elements.append(temp_dict)

    date = datetime.datetime.now()
    question_json = {'answers': question_elements,
                     'questions': questions,
                     'date_created': date.strftime("%Y-%m-%d"),
                     'name': post_dict['quizname']}

    quiz_model.quizjson = json.dumps(question_json)
    quiz_model.subject = post_dict['quizsubject']
    quiz_model.name = post_dict['quizname']
    quiz_model.save()

    return HttpResponseRedirect('/quizzes/create_quiz')


class Quizzes:
    """
    Deprecated method class to load quizzes directly from
    json file located in static folder
    """
    def __init__(self, host):
        self.raw_json = requests.get('http://' + host + '/api/v1/quizdata')
        self.json_obj = json.loads(self.raw_json.text)

    def collect_quiz(self, quiz_id):
        quiz_json = self.json_obj
        quiz_count = len(quiz_json)
        quiz_names = []
        for quiz in quiz_json:
            quiz_names.append(quiz['name'])

        for quiz in quiz_json:
            if str(quiz['id']) == str(quiz_id):
                return quiz, quiz_count, quiz_names

    def get_most_recent_quiz(self):
        return self.json_obj[len(self.json_obj)-1]

    def get_quiz_names(self):
        return [obj['name'] for obj in self.json_obj]