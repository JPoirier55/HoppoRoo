from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
import utils
import json
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


def create_quiz_ap(request):
    dict = json.dumps(request.POST)
    json_dict = json.loads(dict)
    with open('HLS/templates/quizdata.json', 'r') as f:
        quizjson = json.loads(f.read())

    newjson = {"id": len(quizjson),
               "name": json_dict['name'][0],
               "date_created": datetime.datetime.now().strftime('%Y-%m-%d'),
               "questions": json_dict['question'],
               "answers": []}

    for entry_index in range(len(json_dict['question'])):
        tempdict = {"correct": json_dict['correct'][entry_index],
                    "choices": [json_dict['choice_1'][entry_index],
                                json_dict['choice_2'][entry_index],
                                json_dict['choice_3'][entry_index],
                                json_dict['choice_4'][entry_index]]}
        newjson['answers'].append(tempdict)

    quizjson.append(newjson)

    with open("HLS/templates/quizdata.json", "w") as f:
        json.dump(quizjson, f)

    return HttpResponseRedirect('/create_quiz')


def create_quiz(request):
    return render(request, 'create_quiz.html')








# Test page that shows inheritance
def test(request):
    print 'loading test panel'
    return render(request, 'testpanel.html')

