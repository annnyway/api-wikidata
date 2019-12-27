# from django.http import HttpResponse
from django.shortcuts import render
from jsonrpcclient import request as req
from jsonrpcclient.exceptions import ReceivedErrorResponseError
from django.http import JsonResponse
from django.core import serializers
import json
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import Context



# from pprint import pprint


def query(request):
	return render(request, "search.html")

def json_result(request):

	data = request.GET["q"]
	data = [i.strip() for i in data.split(",")]

	try:
		response = req("http://127.0.0.1:5000/", "search", ngrams=data)
		output = json.loads(response.data.result)

		output_ngrams = ", ".join(output["ngrams"])
		wiki_entities = ", ".join([i["wiki_entity"] for i in output["search_result"]])

		result = JsonResponse({"ngram": output_ngrams, "wiki_entity": wiki_entities}) 
	
	except ReceivedErrorResponseError:
		result = JsonResponse({"error": "Sorry, ngrams not found!", "ngram":"", "wiki_entity":""})

	return result