# api-wikidata

This is going to be a web-application for visualizing events from Wikidata that caused frequency growth in the Russian Google Ngrams. 

### Usage:
1. In the first Terminal window run the following commands:
```
cd api
python3 app.py
```
or 
```
cd api
flask run
```
Now the Wikidata API is running on the local host. You can make queries to SQLite database and get data about unigrams. 

2. In the second Terminal window run other commands:
```
cd backend
python3 manage.py runserver
```
Now the web-application scratch is running on your local host. Look at http://127.0.0.1:8000/search/ (or use the other port mentioned in the Terminal window, if 8000 is busy). 

Enter some Russian word in the form. For example, "антипротон". If the word is in the database, it will return the result "антипротон". It will do nothing otherwise. 




