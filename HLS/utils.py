import requests
import json


def collect_quiz(quiz_id, host):
    raw_json = requests.get('http://' + host + '/api/v1/quizdata')
    quiz_json = json.loads(raw_json.text)
    quiz_count = len(quiz_json)
    quiz_names = []
    for quiz in quiz_json:
        quiz_names.append(quiz['name'])

    for quiz in quiz_json:
        if str(quiz['id']) == str(quiz_id):
            return quiz, quiz_count, quiz_names
