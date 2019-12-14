# from django.http import HttpResponse
from django.shortcuts import render
from jsonrpcclient import request as req
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
	
	# try:
	data = request.GET["q"]
	#except 
	response = req("http://127.0.0.1:5000/", "search", ngrams=[data])
	data = json.loads(response.data.result)
	print(data)
	ngrams = ", ".join(data["ngrams"])

	# return render(request, "search.html", context)
	# return JsonResponse({"ngram": response.data.result)})
	return JsonResponse({"ngram": ngrams}) 

#	return render(request, "search.html", json.dumps(data))
#	app.get('result_json', function (req, res) {
#	res.json({ "ngram": 'hi' }