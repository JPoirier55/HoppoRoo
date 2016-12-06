"""
    Utility module for results

    Author: Jake Poirier
    Date: 8/12/16
"""
import math
import os
import requests
import json
from django.http import HttpResponseBadRequest
from django.shortcuts import HttpResponse, HttpResponseRedirect


def median(scores):
    """
    Computes median of a list of scores
    :param scores: list of scores
    :return: median of that list
    """
    if len(scores) == 0:
        return 0
    scores = sorted(scores)
    return scores[((len(scores)+1) / 2) - 1]


def std_deviation(scores, mean):
    """
    Computes std deviation of a list of scores
    :param scores: list of scores
    :param mean: median of that list
    :return: stnd deviation of the list
    """
    if len(scores) == 0:
        return 0
    numerator = math.fsum([math.pow(score - mean, 2) for score in scores])
    denominator = len(scores)
    return round(math.sqrt((numerator/denominator)), 2)


def average(scores):
    """
    Computes average/mean of list
    :param scores: list of scores
    :return: mean of list
    """
    sum = 0
    if len(scores) == 0:
        return 0
    for score in scores:
        sum += score
    return sum / len(scores)


def upload(request):
    """
    Generic upload method to write a file from
    http to the system at a specific directory.
    Directory in this case has been set to res
    because of the permissions in http
    :param request: wagi request
    :return: HTTP response for upload
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


def delete(request):
    """
    Generic delete method for deleting files off the
    system. Requires directory depending on
    where the file is located, but here is an API
    method which handles finding the file in res
    :param request: wsgi request
    :return: HTTP response for delete
    """
    filename = request.GET.get('filename')
    redirect = request.GET.get('redirect')
    try:
        os.remove(filename)
        return HttpResponseRedirect("/" + redirect)
    except IOError as e:
        return HttpResponseBadRequest('PDF DELETE ERROR:{0}'.format(e.strerror))


def data_api_method(ip_arr):
    """
    API method for collection data from mats.
    Does a round robin on the mats that are connected
    to the system via search ip script. All data
    is aggregated into a dict and sent back to
    view method
    :param ip_arr: list of ips connected to system
    :return: array of mat data
    """
    a = 0
    b = 0
    c = 0
    d = 0
    nodes = {}
    for ip in ip_arr:
        try:
            response_data = json.loads(requests.get("http://{0}:8080".format(ip)).text)
            a += int(response_data['buttonA'])
            b += int(response_data['buttonB'])
            c += int(response_data['buttonC'])
            d += int(response_data['buttonD'])

            nodes[response_data['id']] = response_data
        except requests.RequestException:
            return json.dumps({})

    output_json = {'A': a,
                   'B': b,
                   'C': c,
                   'D': d,
                   'node_data': nodes}
    return json.dumps(output_json)
