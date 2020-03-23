from jsonrpcclient import request
from pprint import pprint

if __name__ == "__main__":
    
    response = request("http://0.0.0.0:5000/", "search", ngrams=["россия"])
    pprint(response.data.result)
