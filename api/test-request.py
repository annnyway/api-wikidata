from jsonrpcclient import request
from pprint import pprint

if __name__ == "__main__":
    
    response = request("http://127.0.0.1:5000/", "search", ngrams=["россия"])
    pprint(response.data.result)
