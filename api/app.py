from pymystem3 import Mystem
from string import punctuation
from jsonrpc.backend.flask import api
from flask import Flask
from jsonrpc.exceptions import JSONRPCDispatchException
# from jsonrpcserver import method, dispatch
import json

from hseling_api_wikidata.database_search import DatabaseSearch, NotFoundError
from hseling_api_wikidata.connect_to_db import connect

punct = punctuation+'«»—…“”*–'
morph = Mystem()

app = Flask(__name__)
app.register_blueprint(api.as_blueprint())
app.add_url_rule('/', 'search', api.as_view(), methods=['POST'])
app.add_url_rule('/', 'datasets', api.as_view())


#class NotFoundException(JSONRPCDispatchException):
#    def __init__(self, code=404, message="Ngrams not found"):
#        self.code = code
#        self.message = message

@api.dispatcher.add_method
def search(ngrams:list):
    cursor = connect("wikidata.db")
    try: 
        data = DatabaseSearch(ngrams=ngrams, 
                          morph=morph, 
                          punct=punct,
                          cursor=cursor)
        search_result = data.sql_result
        coordinates = data.coordinates
        return json.dumps({"ngrams": ngrams, 
                "search_result": search_result, 
                "coordinates": coordinates})
    except NotFoundError:
#        raise NotFoundException
        raise JSONRPCDispatchException(code=404, message="Ngrams not found")


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True, port=80)
    app.run(debug=True)
