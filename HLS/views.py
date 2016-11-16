
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
from results import results_process_questions
from results import results_process_data
from models import Quiz, Results, PDFQuiz, Student, Device
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from scripts import set_ip_adds
import xlsxwriter


def test_page(request):
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

    return render(request, 'question_view.html', {'quizname': selected_quiz,
                                                  'question_num': question_num,
                                                  'show_correct': show_correct,
                                                  'question': question,
                                                  'choice_a': choice_a,
                                                  'choice_b': choice_b,
                                                  'choice_c': choice_c,
                                                  'choice_d': choice_d})


# @login_required(login_url='/login/')
def load_quiz(request):
    """
    Page to load and view quizzes
    :param request: wsgi request
    :return: rendered load quiz page
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

    return render(request, 'load_quiz.html', {'chosen_quiz': quiz_obj,
                                              'quiz_ids': quiz_ids,
                                              'quiz_names': quiz_names,
                                              'qt': qt})


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
    pdfs = []
    dir = '/home/pi/HoppoRoo/HoppoRoo/static/res/'
    # dir = 'C:\\Users\\Jake\\git3\\HoppoRoo\\static\\res\\'
    for pdf in os.listdir(dir):
        if 'pdf' in pdf:
            pdf = {'name': pdf,
                   'dir': dir+pdf}
            pdfs.append(pdf)
    return render(request, 'pdf_view.html', {'pdfs': pdfs})


def pdf_upload(request):
    """
    Page to upload pdfs as quizzes and see the current pdfs that
    are on the system
    :param request: wsgi request
    :return: rendered pdf upload page and pdf filenames
    """
    pdfs = []
    dir = '/home/pi/HoppoRoo/HoppoRoo/static/res/'
    # dir = 'C:\\Users\\Jake\\git3\\HoppoRoo\\static\\res\\'
    for pdf in os.listdir(dir):
        if 'pdf' in pdf:
            pdf = {'name': pdf,
                   'dir': dir + pdf}
            pdfs.append(pdf)
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
    student_objs = Student.objects.all()
    names = [student.name for student in student_objs]

    results_arr = []

    if 'name' not in request.GET:
        student_name = names[0]
    else:
        student_name = request.GET['name']

    student_obj = Student.objects.get(name=student_name)
    results_objs = Results.objects.filter(student__name=student_obj.name)

    for result in results_objs:
        quiz_dict = {'quiz': result.quiz.name,
                     'quiz_id': result.quiz.id,
                     'score': result.score}
        results_arr.append(quiz_dict)

    return render(request, 'students.html', {'student_list': names,
                                             'chosen_student': student_name,
                                             'results': results_arr,
                                             })


def students(request):
    devices = Device.objects.all()
    return render(request, 'students1.html', {'devices': devices})


def students_add(request):
    return render(request, 'student_add.html')


# ---------------------- API SECTION ----------------- #


@csrf_exempt
def upload_file(request):
    """
    API method to upload file from pdf upload page
    :param request: wsgi request
    :return: response for upload
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST requests are allowed')
    file = request.FILES['myfile']
    dir = '/home/pi/HoppoRoo/HoppoRoo/static/res/'
    # dir = 'C:\\Users\\Jake\\git3\\HoppoRoo\\static\\res\\'
    with open(dir+'%s' % file.name, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    return HttpResponse("file uploaded")


def delete_file(request):
    """
    API method to delete files from pdf view page
    :param request: wsgi request
    :return: response for delete
    """
    filename = request.GET.get('filename')
    redirect = request.GET.get('redirect')
    try:
        os.remove(filename)
        return HttpResponseRedirect("/"+redirect)
    except IOError as e:
        return HttpResponseBadRequest('PDF DELETE ERROR:{0}'.format(e.strerror))


def serve_quiz(request):
    quizzes = Quiz.objects.all()
    quiz_json = []
    for quiz in quizzes:
        quiz_json.append(quiz.quizjson)
    return HttpResponse(json.dumps(quiz_json))


@csrf_exempt
def result_post_point(request):
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
            #obj, create = Results.objects.update_or_create(quiz=quiz_obj, student=device.student, score=score)
	    result = Results()
            result.quiz = quiz_obj
            result.student = device.student
            result.score = score
            result.save()
        except Exception:
            return HttpResponse("failure")

    return HttpResponse("success")


def data_access_point(request):
    """
    Point that holds and updates all mat data and consolidates it
    into one json object that is then served
    :param request: request from current page
    :return: response object with json data
    """
    ip_arr = set_ip_adds.parse_nmap()
    response_data = {}
    a = 0
    b = 0
    c = 0
    d = 0
    nodes = {}
    for ip in ip_arr:
	print ip
        try:
            response_data = json.loads(requests.get("http://{0}:8080".format(ip)).text)
            a += int(response_data['buttonA'])
            b += int(response_data['buttonB'])
            c += int(response_data['buttonC'])
            d += int(response_data['buttonD'])

            nodes[response_data['id']] = response_data
        except requests.RequestException:
            return HttpResponse(json.dumps({}))
    # output_json = {'A': 1,
    #                'B': 2,
    #                'C': 4,
    #                'D': 3,
    #                'node_data': 'testse'}
    output_json = {'A': a,
                   'B': b,
                   'C': c,
                   'D': d,
                   'node_data': nodes}

    # return HttpResponse(json.dumps({"A": 0, "node_data": {"55555": {"buttonC": "0", "buttonB": "1", "buttonA": "0", "buttonD": "0"},
    #                                                       "12345": {"buttonC": "0", "buttonB": "0", "buttonA": "1", "buttonD": "0"},
    #                                                       "11111": {"buttonC": "0", "buttonB": "0", "buttonA": "0", "buttonD": "1"}},
    #                                 "C": 0, "B": 1, "D": 0}))
    return HttpResponse(json.dumps(output_json))


def create_quiz_ap(request):
    """
    Quiz data access point for storing and retrieving quiz data
    :param request: request from current page
    :return: redirect back to page while
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
                         'correct': post_dict['question'+index]}
            question_elements.append(temp_dict)
    else:
        for i in range(question_count):
            index = str(i)
            quiz_model = Quiz()
            questions.append(post_dict['question'+index])
            temp_dict = {'correct': post_dict['correct'+index],
                         'choices': [post_dict['choice1'+index],
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


def quiz_data(request):
    name = request.GET.get('quizname')
    quizzes = Quiz.objects.all()
    quiz_arr = []
    for quiz in quizzes:
        if quiz.name == name:
            quiz_arr.append(quiz.quizjson)

    return HttpResponse(json.dumps(quiz_arr), content_type="application/json")


def add_student_device(request):
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
            worksheet.write(0, quiz.id+3, quiz.name, bold)

        for index in range(len(devices)):
            worksheet.write(index + 1, 1, devices[index].student.name)
            worksheet.write(index + 1, 2, devices[index].student.id)
            worksheet.write(index + 1, 3, devices[index].id)
            for result in results:
                for quiz in quizzes:
                    if devices[index].student.name == result.student.name and result.quiz.name == quiz.name:
                        worksheet.write(index + 1, quiz.id+3, result.score)

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


