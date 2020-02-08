# from django.http import HttpResponse
from django.shortcuts import render
from jsonrpcclient import request as req
from jsonrpcclient.exceptions import ReceivedErrorResponseError
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import Context
import pandas as pd
from . import HTML

def query(request):
    return render(request, "search.html")


def json_result(request):

    data = request.GET["q"]
    data = [i.strip() for i in data.split(",")]

    try:
        response = req("http://127.0.0.1:5000/", "search", ngrams=data)
        output = json.loads(response.data.result)
        coords = output["coordinates"]
        str_coords = []


        # prepare coordinates for drawing a graph
        for ngram_coord in coords:
            x = ",".join([str(l[1]) for l in ngram_coord])
            y = ",".join([str(l[2]) for l in ngram_coord])
            labels = ",".join([str(l[0]) for l in ngram_coord])
            res = "|".join([x,y,labels])
            str_coords.append(res)

        if len(str_coords) > 1:
            str_coords = "||".join(str_coords)
        else:
            str_coords = "||" + str_coords[0]



        # (CURRENTLY!) prepare table data
        d = {"#":[], "Ngram":[], "Wiki Entity":[], "#Q":[], "#P":[], "Property":[], "Object":[], 
                "Organization":[], "Date":[], "Start Time":[], "End Time":[], "Time Point":[], "Growth Speed":[]}

        search_result = output["dict_result"]

        table_data = []

        for item in search_result:
            cur_list = []
            cur_list.append(int(item["entry_id"]+1))
            cur_list.append(item["ngram"])
            cur_list.append(item["wiki_entity"])
            cur_list.append(item["Q_number"])
            cur_list.append(item["property_code"])
            cur_list.append(item["property_value"])
            cur_list.append(item["object"])
            cur_list.append(item["organization"])
            cur_list.append(item["just_date"])
            cur_list.append(item["start_time"])
            cur_list.append(item["end_time"])
            cur_list.append(item["time_point"])
            cur_list.append(round(item["growth_speed"],2))

            table_data.append(cur_list)

        html_table = HTML.table(table_data)
        header = """
  <table class="table table-striped table-bordered table-sm">
    <thead class="thead-dark">
            <tr>
              <th>#</th>
              <th>Ngram</th>
              <th>Wiki Entity</th>
              <th>#Q</th>
              <th>#P</th>
              <th>Property</th>
              <th>Object</th>
              <th>Organization</th>
              <th>Date</th>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Time Point</th>
              <th>Growth Speed</th>
            </tr>
          </thead>
    <tbody> """
        new_table = header + html_table[105:-15] + """</tbody></table>"""
        csv_data = output["csv_result"]
        result = JsonResponse({"ngram":new_table, "coords":str_coords, "csv":csv_data})
    except ReceivedErrorResponseError:
        result = JsonResponse({"error": "Sorry, ngrams not found! Try again.", "ngram":""})

    return result

