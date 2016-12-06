from models import Student, Results


def student_results(request):
    """
    Build dictionary with all student data
    and results from quizzes
    :param request: wsgi request
    :return: results array with student data
    """
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

    return {'student_list': names,
            'chosen_student': student_name,
            'results': results_arr,
            }

