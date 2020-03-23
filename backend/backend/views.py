from django.shortcuts import render
from jsonrpcclient import request as req
from jsonrpcclient.exceptions import ReceivedErrorResponseError
import json
from django.http import JsonResponse
import pandas as pd
from io import StringIO


def query(request):
    return render(request, "search.html")

def clustersearch(request):
    return render(request, "clustersearch.html")

def datasets(request):
    return render(request, "datasets.html")

def json_result_plot(request):
    res = request.GET




    try:
        response = req("http://toma-api:5000/", "clustersearch", data=res)
        output = json.loads(response.data.result)
        words = output['ngrams']
        result = []
        x = list(range(1918,2010))

        # prepare coordinates for drawing a graph
        for i in range(len(words)):
            y = output['frequencies'][i]
            label = words[i]
            result.append({'x':x, 'y':y, 'type': 'scatter', 'name':label})

        result = JsonResponse({"coords":result})

    except ReceivedErrorResponseError:
        result = JsonResponse({"error": "Sorry, ngrams not found! Try again.", "ngram":""})

    return result


def json_result(request):

    data = request.GET["q"]
    data = [i.strip() for i in data.split(",")]

    try:
        response = req("http://toma-api:5000/", "search", ngrams = data)
        output = json.loads(response.data.result)
        csv_data = output["csv_result"]
        test_data = StringIO(csv_data)
        table_data = pd.read_csv(test_data).iloc[:, 2:].to_html()
        table_data = table_data[51:-19]
        header = """<table class="table table-striped table-bordered table-sm">
        <thead class="thead-dark">"""
        table_data = header + table_data + """</tbody></table>
        <button type="button" name="btn" id="btn" class="btn btn-dark" onClick="exportTableToCSV('results.csv')">
        Download CSV</button>"""
        result = JsonResponse({"table": table_data, "csv": csv_data})

    except ReceivedErrorResponseError:
        result = JsonResponse({"error": "Sorry, ngrams not found! Try again.", "ngram": ""})

    return result

