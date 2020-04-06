from django.shortcuts import render
from jsonrpcclient import request as req
from jsonrpcclient.exceptions import ReceivedErrorResponseError
import json
from django.http import JsonResponse
import pandas as pd
from io import StringIO


def landing(request):
    return render(request, "landing.html")

def query(request):
    return render(request, "wikingram.html")


def clustersearch(request):
    return render(request, "similarity.html")


def datasets(request):
    return render(request, "datasets.html")


def wiki_instruction(request):
    return render(request, "wiki-instruction.html")


def json_result(request):
    data = request.GET["q"]
    data = [i.strip() for i in data.split(",")]

    try:
        response = req("http://127.0.0.1:5000/", "search", ngrams=data)
        output = json.loads(response.data.result)
        csv_data = output["csv_result"]
        test_data = StringIO(csv_data)
        df = pd.read_csv(test_data).iloc[:, 2:]

        table_data = df.to_html()
        table_data = table_data[51:-19]
        header = """<button type="button" name="btn" id="btn" class="btn btn-dark" align="center" onClick="exportTableToCSV('result.csv')">
        Download CSV</button>
        <br><br>
        <table class="table table-striped table-bordered table-sm d-none">
        <thead class="thead-dark">"""
        table_data = header + table_data + """</tbody></table>"""
        df = df.fillna("nan")
        csv_data = df.to_csv(header=False)

        wiki_df = df[["ngram", "Q_number"]]
        wiki_df = wiki_df.drop_duplicates()
        wiki_df.reset_index(inplace=True, drop=True)

        groups = wiki_df.groupby(by="ngram", as_index=False)
        group_dict = {}
        for group in groups:
            group_dict[group[0]] = group[1].Q_number.tolist()
        wiki_list = dict_to_html(group_dict)

        result = JsonResponse({"table": table_data, "csv": csv_data, "wiki": wiki_list})

    except ReceivedErrorResponseError:
        result = JsonResponse({"error": "Sorry, ngrams not found! Try again.", "ngram": ""})

    return result


def json_result_plot(request):
    res = request.GET

    try:
        response = req("http://127.0.0.1:5000/", "clustersearch", data=res)
        output = json.loads(response.data.result)
        # print('Printing output in views', output)


        words = output['ngrams']
        print('words:', words)
        result = []
        x = list(range(*output['years'])) #list(range(1880,2010))

        # prepare coordinates for drawing a graph
        for i in range(len(words)):
            y = output['frequencies'][i]
            label = words[i]
            result.append({'x':x, 'y':y, 'type': 'scatter', 'name':label})

        result = JsonResponse({"coords":result})

    except ReceivedErrorResponseError:
    # except:
        print('Error in views')
        # print('Error in views', sys.exc_info()[0])
        result = JsonResponse({"error": "Sorry, ngrams not found! Try again.", "ngram":""})

    return result


def dict_to_html(d:dict):
    new_list = '<br><br><p align="center"><b>Сущности в Викиданных:</b></p><br><div class="card" style="width: 18rem;"><ul class="list-group list-group-flush">'
    keys = sorted(list(d.keys()))
    for key in keys:
        vals = d[key]
        vals = ['<a href="https://www.wikidata.org/wiki/{}">{}</a>'.format(x, x) for x in vals]
        new_list += '<li class="list-group-item">' + key + ": " + ", ".join(vals) + "</li>"
    new_list += """</ul></div><br><br><button type="button" name="btn" id="save_table_btn" class="btn text-white" style="background-color:#476f93" onClick="exportTableToCSV('result.csv')" align="bottom">Скачать данные в виде csv-таблицы</button>
"""
    return new_list
