from pymystem3 import Mystem
from string import punctuation
from jsonrpc.backend.flask import api
from flask import Flask
from jsonrpc.exceptions import JSONRPCDispatchException
import json
import os.path
from hseling_api_wikidata.database_search import DatabaseSearch, NotFoundError
from hseling_api_wikidata.connect_to_db import connect

from get_data import get_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

punct = punctuation + '«»—…“”*–'
morph = Mystem()

app = Flask(__name__)
app.register_blueprint(api.as_blueprint())
app.add_url_rule('/', 'search', api.as_view(), methods=['POST'])


@api.dispatcher.add_method
def search(ngrams: list):
    cursor = connect(os.path.join(BASE_DIR, "wikidata.db"))
    try:
        data = DatabaseSearch(ngrams=ngrams,
                              morph=morph,
                              punct=punct,
                              cursor=cursor)
        return json.dumps({"ngrams": data.ngrams,
                           "csv_result": data.csv_format})
    except NotFoundError:
        raise JSONRPCDispatchException(code=404, message="Ngrams not found")

app.add_url_rule('/', 'clustersearch', api.as_view(), methods=['POST'])

@api.dispatcher.add_method
def clustersearch(data: dict):
    ngram = data["q"]
    sim = data["sim"]
    freq = data["freq"]

    try:
        data = get_data(ngram=ngram, sim=sim, freq=freq)
        return json.dumps(data)
    except NotFoundError:
        raise JSONRPCDispatchException(code=404, message="Ngrams not found")

if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True, port=80)
    app.run(debug=True)

