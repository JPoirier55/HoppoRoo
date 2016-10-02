from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
import utils
import json
import datetime
from models import Quiz, Results
import sys
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from models import Student
from results import results_metrics
from quizzes import Quizzes


def test_page(request):
    numpages = 5
    quizzest = Quiz.objects.all()


    return render(request, 'testingpage.html', {'numpages': len(quizzest),
                                                'quizzes': quizzest})

def auth_view(request):
    username = request.POST.get('Username', '')
    password = request.POST.get('Password', '')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        print 'user logged in'
        return HttpResponseRedirect('/home/')
    else:
        print 'error'
        return HttpResponseRedirect('/login/')


def logout_view(request):
    logout(request)
    msg = 'you have been loggd out'
    return render(request, 'registration/login.html', {'msg': msg})


def login_view(request):
    print HttpResponse()
    return render(request, 'registration/login.html')


# @login_required(login_url='/login/')
def home(request):
    """
    Home page with access to most recent quiz and the ability to login
    :param request: request from current page
    :return: rendered template with data
    """
    quiz_obj = Quizzes(request.META['HTTP_HOST'])
    chosen_quiz = quiz_obj.get_most_recent_quiz()
    return render(request, 'home.html', {'recent_quiz': chosen_quiz,
                                         'quiz_name': chosen_quiz['name']})


# @login_required(login_url='/login/')
def quizzes_home(request):
    return render(request, 'quizzes_home.html')


# @login_required(login_url='/login/')
def quizzes(request):
    return render(request, 'quiz_view_1.html')


# @login_required(login_url='/login/')
def quiz_view(request):
    quiz = requests.get("http://192.168.42.1/api/v1/quizdata")
    quiz = json.loads(quiz.text)	
    return render(request, 'quiz_view_1.html', {'quiz': quiz[0]})


# @login_required(login_url='/login/')
def load_quiz(request):
    """
    Page to load and view quizzes
    :param request: request from current page
    :return: redered template for load quiz page
    """
    if 'id' in request.GET:
        id = request.GET['id']
    else:
        id = 0
    quiz_obj = Quizzes(request.META['HTTP_HOST'])

    return render(request, 'load_quiz.html', {'chosen_quiz': quiz_obj.json_obj[int(id)],
                                              'quiz_count': range(len(quiz_obj.json_obj)),
                                              'quiz_names': quiz_obj.get_quiz_names()})


# @login_required(login_url='/login/')
def create_quiz(request):
    """
    Page that allows user to create quiz and save it
    :param request: request from current page
    :return: rendered template for create quiz page
    """
    if request.GET.get('subject'):
        subject = request.GET.get('subject')
    else:
        subject = ''
    return render(request, 'create_quiz1.html', {'subject': subject})


def build_quiz(request):
    param_dict = request.GET
    print param_dict

    return render(request, 'build_quiz.html', {'name': param_dict['name'],
                                               'numquestions': int(param_dict['numquestions']),
                                               'subject': param_dict['subject']})


# @login_required(login_url='/login/')
def help(request):
    return render(request, 'help.html')

def pdf_view(request):
    return render(request, 'pdf_view.html')

# @login_required(login_url='/login/')
def results(request):
    metrics = results_metrics()
    return render(request, 'results.html', {'results_list': metrics})


# @login_required(login_url='/login/')
def students(request):
    student_objs = Student.objects.all()
    names = [student.name for student in student_objs]

    results_arr = []

    if 'name' not in request.GET:
        student_name = names[0]
    else:
        student_name = request.GET['name']

    student_obj = Student.objects.get(name=student_name)
    results = Results.objects.filter(student__name=student_obj.name)

    for result in results:
        quiz_dict = {'quiz': result.quiz.name,
                     'quiz_id': result.quiz.id,
                     'score': result.score}
        results_arr.append(quiz_dict)

    return render(request, 'students.html', {'student_list': names,
                                             'chosen_student': student_name,
                                             'results': results_arr,
                                             })


# ---------------------- API SECTION ----------------- #
def data_access_point(request):
    """
    Point that holds and updates all mat data and consolidates it
    into one json object that is then served
    :param request: request from current page
    :return: response object with json data
    """
    response_data = json.loads(requests.get("http://192.168.42.19:8080").text)
    response_data3 = json.loads(requests.get("http://192.168.42.18:8080").text)

    output_json = {'A': int(response_data['buttonA'])+int(response_data3['buttonA']),
                   'B': int(response_data['buttonB'])+int(response_data3['buttonB']),
                   'C': int(response_data['buttonC'])+int(response_data3['buttonC']),
                   'D': int(response_data['buttonD'])+int(response_data3['buttonD'])}

    return HttpResponse(json.dumps(output_json))


def create_quiz_ap(request):
    """
    Quiz data access point for storing and retrieving quiz data
    :param request: request from current page
    :return: redirect back to page while
    """



    post_dict = request.POST
    question_count = 0
    question_elements = []
    for key,value in post_dict.iteritems():
        if 'question' in key:
            question_count += 1
    for i in range(question_count):
        index = str(i)
        temp_dict = {'question': post_dict['question'+index],
                     'correct': post_dict['correct'+index],
                     'choice1': post_dict['choice1'+index],
                     'choice2': post_dict['choice2' + index],
                     'choice3': post_dict['choice3' + index],
                     'choice4': post_dict['choice4' + index]}
        question_elements.append(temp_dict)
    print question_elements







    # quiz_model.save()


    return HttpResponseRedirect('/create_quiz')


def quiz_data(request):
    return render(request, 'quizdata.json')
