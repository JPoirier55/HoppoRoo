import requests
import json

class Quizzes:
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
