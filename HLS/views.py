from django.shortcuts import render
import utils
import datetime


def index(request):
    return render(request, 'index.html')


def quiz_view(request):
    return render(request, 'quiz_view.html')


def load_quiz(request):
    if 'id' in request.GET:
        id = request.GET['id']
    else:
        id = 0
    host = request.META['HTTP_HOST']
    chosen_quiz, quiz_count, quiz_names = utils.collect_quiz(id, host)

    return render(request, 'load_quiz.html', {'chosen_quiz': chosen_quiz,
                                              'quiz_count': range(quiz_count),
                                              'quiz_names': quiz_names})


def quiz_data(request):
    return render(request, 'quizdata.json')





# Test page that shows inheritance
def test(request):
    print 'loading test panel'
    return render(request, 'testpanel.html')

