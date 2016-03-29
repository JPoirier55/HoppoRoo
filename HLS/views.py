from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
import utils
import json
import datetime
from models import Quiz
import sys


def home(request):
    quiz_obj = utils.Quizzes(request.META['HTTP_HOST'])
    chosen_quiz = quiz_obj.get_most_recent_quiz()
    return render(request, 'home.html', {'recent_quiz': chosen_quiz,
                                         'quiz_name': chosen_quiz['name']})


def quiz_view(request):
    return render(request, 'quiz_view.html')


def load_quiz(request):
    if 'id' in request.GET:
        id = request.GET['id']
    else:
        id = 0
    quiz_obj = utils.Quizzes(request.META['HTTP_HOST'])

    return render(request, 'load_quiz.html', {'chosen_quiz': quiz_obj.json_obj[int(id)],
                                              'quiz_count': range(len(quiz_obj.json_obj)),
                                              'quiz_names': quiz_obj.get_quiz_names()})


def quiz_data(request):
    return render(request, 'quizdata.json')


def create_quiz_ap(request):
    dict = json.dumps(request.POST)
    json_dict = json.loads(dict)

    try:
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

        quiz_model = Quiz()
        quiz_model.quizjson = json.dumps(newjson)
        quiz_model.save()

        with open("HLS/templates/quizdata.json", "w") as f:
            json.dump(quizjson, f)
    except Exception, e:
        sys.stderr("Cannot do something")

    return HttpResponseRedirect('/create_quiz')


def create_quiz(request):
    return render(request, 'create_quiz.html')
