
"""
    Views module: Each page is rendered from this module and corresponds
    to the url defined in urls.py

    Author: Jake Poirier
    Date: 2/15/16
"""

import os
import json
import datetime
import requests
import quiz_utils, student_utils, utils, results_utils
from models import Quiz, Results, PDFQuiz, Student, Device
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from scripts import set_ip_adds
import xlsxwriter


def test_page(request):
    """
    For testing purposes only
    :param request: wsgi request
    :return: render test page
    """
    numpages = 5
    quizzest = Quiz.objects.all()
    return render(request, 'testingpage.html', {'numpages': len(quizzest),
                                                'quizzes': quizzest})


def auth_view(request):
    """
    Authorization page: Currently not in use, will be implemented
    if priority calls for it
    :param request: wsgi request
    :return: http response redirect to home or login if incorrect creds
    """
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
    """
    View to handle logout template
    :param request: wsgi request
    :return: render login page
    """
    logout(request)
    msg = 'you have been logged out'
    return render(request, 'registration/login.html', {'msg': msg})


def login_view(request):
    """
    View to handle logging in template
    :param request: wsgi request
    :return: render login page
    """
    print HttpResponse()
    return render(request, 'registration/login.html')


# @login_required(login_url='/login/')
def home(request):
    """
    Home page with access to most recent quiz and the ability to login
    :param request: request from current page
    :return: rendered template with data
    """
    return render(request, 'home.html')


# @login_required(login_url='/login/')
def quizzes_home(request):
    """
    Quiz home page where teacher can choose either create or
    view quiz, and create with subject
    :param request: wsgi request
    :return: rendered quizzes home page
    """
    return render(request, 'quizzes_home.html')


def choose_quiz(request):
    """
    Page to choose quiz from pull down
    for use in quiz view
    :param request: wsgi request
    :return: render choose quiz page
    """
    quizzes = Quiz.objects.all()
    quiz_names = []
    for quiz in quizzes:
        quiz_names.append(quiz.name)
    return render(request, 'choose_quiz.html', {'quiz_names': quiz_names})


# @login_required(login_url='/login/')
def quiz_view(request):
    """
    Quiz view page which shows the real time graph of quiz input
    and shows the quiz questions and choices
    :param request: wsgi request
    :return: rendered quiz view page
    """
    set_ip_adds.run_nmap()
    selected_quiz = request.GET.get('quizname')
    quiz = Quiz.objects.get(name=selected_quiz)
    quiz_length = len(json.loads(quiz.quizjson)['questions'])
    return render(request, 'quiz_view_1.html', {'quizname': selected_quiz,
                                                'quiz_length': quiz_length,
                                                })


def question_view(request):
    """
    Page to show question outside of controller.
    This is what gets shown on a projector or screen
    outside the teacher's controller view
    :param request: wsgi request
    :return: render question view page
    """
    quiz_dict = quiz_utils.question_builder(request)
    return render(request, 'question_view.html', quiz_dict)


# @login_required(login_url='/login/')
def load_quiz(request):
    """
    Page to load and view quizzes
    :param request: wsgi request
    :return: rendered load quiz page
    """
    quizzes_dict = quiz_utils.quiz_loader(request)

    return render(request, 'load_quiz.html', quizzes_dict)


# @login_required(login_url='/login/')
def create_quiz(request):
    """
    Page that allows user to create quiz and save it
    :param request: wsgi request
    :return: rendered template for create quiz page
    """
    if request.GET.get('subject'):
        subject = request.GET.get('subject')
    else:
        subject = ''
    return render(request, 'create_quiz1.html', {'subject': subject})


def build_quiz(request):
    """
    Page to input quiz questions and answers and review and edit
    the pages after completed
    :param request: wsgi request
    :return: build quiz for either pdf or non-pdf quizzes
    """
    param_dict = request.GET
    if param_dict['pdf'] == 'true':
        return render(request, 'build_quiz_pdf.html', {'name': param_dict['name'],
                                                       'numquestions': int(param_dict['numquestions']),
                                                       'subject': param_dict['subject']})

    return render(request, 'build_quiz.html', {'name': param_dict['name'],
                                               'numquestions': int(param_dict['numquestions']),
                                               'subject': param_dict['subject']})


# @login_required(login_url='/login/')
def help(request):
    """
    Help page for any questions regarding using the app
    :param request:
    :return:
    """
    return render(request, 'help.html')


def pdf_view(request):
    """
    View to show pdf quiz and pdf fullscreen
    :param request: wsgi request
    :return: rendered pdf view page, with pdf filenames
    """
    pdfs = quiz_utils.pdf_builder()
    return render(request, 'pdf_view.html', {'pdfs': pdfs})


def pdf_upload(request):
    """
    Page to upload pdfs as quizzes and see the current pdfs that
    are on the system
    :param request: wsgi request
    :return: rendered pdf upload page and pdf filenames
    """
    pdfs = quiz_utils.pdf_builder()
    return render(request, 'pdf_upload.html', {'pdfs': pdfs})


# @login_required(login_url='/login/')
def results(request):
    """
    Results page which shows all student data for each
    quiz they have taken
    :param request: wsgi request
    :return: results page with quiz metrics metrics data
    """
    results_objs = Results.objects.all()
    students_objs = Student.objects.all()
    chosen_student = request.GET.get('student', 'all')
    return render(request, 'results.html', {'results_list': results_objs,
                                            'students': students_objs,
                                            'chosen_student': chosen_student})


# @login_required(login_url='/login/')
def students_backup(request):
    """
    Deprecated Page showing students data and results
    for quizzes.
    :param request: wsgi request
    :return: render students page
    """
    results_arr = student_utils.student_results(request)
    return render(request, 'students.html', results_arr)


def students(request):
    """
    Page to show students who are paired with
    whatever device. Page allows teacher to add
    new students for a new device
    :param request: wsgi request
    :return: render students page
    """
    devices = Device.objects.all()
    return render(request, 'students1.html', {'devices': devices})


def students_add(request):
    """
    Add page from students page which allows
    adding a new device for a student
    :param request: wsgi request
    :return: render student add page
    """
    return render(request, 'student_add.html')


# ---------------------- API SECTION ----------------- #


@csrf_exempt
def upload_file(request):
    """
    API method to upload file from pdf upload page
    :param request: wsgi request
    :return: response for upload
    """
    # TODO: FIX JQUERY.UPLOAD.MIN.JS TO HANDLE OFFLINE HANDLE OF JQUERY.FORM.JS --> SEE JQUERY.UPLOAD.MIN.JS
    return utils.upload(request)


def delete_file(request):
    """
    API method to delete files from pdf view page
    :param request: wsgi request
    :return: response for delete
    """
    return utils.delete(request)


def serve_quiz(request):
    """
    Deprecated method which serves
    quiz data through api call
    :param request: wsgi request
    :return: HTTP response with json
    """
    return quiz_utils.build_quiz_api()


@csrf_exempt
def result_post_point(request):
    return results_utils.result_post_method(request)


def data_access_point(request):
    """
    Point that holds and updates all mat data and consolidates it
    into one json object that is then served
    :param request: request from current page
    :return: response object with json data
    """
    ip_arr = set_ip_adds.parse_nmap()
    response_data = utils.data_api_method(ip_arr)
    return HttpResponse(response_data)


def create_quiz_ap(request):
    """
    Quiz data access point for storing and retrieving quiz data
    :param request: request from current page
    :return: redirect back to page while
    """
    return quiz_utils.create_quiz_method(request)


def quiz_data(request):
    """
    Simple API method to return data
    from each quiz as one json obj
    :param request: wsgi request
    :return: HTTP resonse with json
    """
    name = request.GET.get('quizname')
    quizzes = Quiz.objects.all()
    quiz_arr = []
    for quiz in quizzes:
        if quiz.name == name:
            quiz_arr.append(quiz.quizjson)

    return HttpResponse(json.dumps(quiz_arr), content_type="application/json")


def add_student_device(request):
    """
    API method to handle incoming form POST
    for adding a new student to the database
    with a certain Device foreign key
    :param request: wsgi request
    :return: redirect or error message
    """
    post_dict = request.POST
    try:
        student = Student()
        student.id = post_dict['student_id']
        student.name = post_dict['student_name']
        student.save()
        device = Device()
        device.id = post_dict['device_id']
        device.student = student
        device.save()
        return HttpResponseRedirect('/students')
    except Exception as e:
        error_message = '''Failure adding student to database. Try again and make sure inputs are correct,
                         student IDs are not duplicated and all fields have been filled out.'''
        return render(request, 'generic_error.html', {"error_message": error_message,
                                                      "return": '/students'})


def export_xlsx(request):
    """
    API method to handle exporting
    xlsx from results page
    :param request: wsgi request
    :return: render method for response
    """
    return results_utils.xlsx_handler(request)



