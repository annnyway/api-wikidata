import json
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def connect_to_db(path_to_db):
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    return cursor

def get_from_db(cursor, ngram, col):
    res = cursor.execute("""SELECT {} from FREQUENCIES where ngram='{}'""".format(col, ngram)).fetchall()
    res = json.loads(res[0][0])
    if type(res) == dict:
        res = [list(i) for i in sorted(res.items(), key=lambda x:x[1], reverse=True)]
    return res


def get_data(ngram, freq="rel", sim="cosine"):
    n = 0
    if sim == 'dtw':
        n = 1
    
    sim = "top_{}_{}".format(sim, freq)
    freq = "rows_" + freq
    
    path_to_db = os.path.join(BASE_DIR, "ngrams.db")
    cursor = connect_to_db(path_to_db)
    
    sims = get_from_db(cursor=cursor, ngram=ngram.lower(), col=sim)

    # print('\n\n', sims, '\n\n')
    res = {'ngrams':[], 'frequencies':[], 'similarities':[]}
    if n == 1:
        sims = [[i[0], n - i[1]] for i in sims]
    print(sims)
    
    for arr in sorted(sims, key=lambda x:x[1], reverse=True):
        
        word = arr[0]
        how_similar = arr[1]

            
        word = cursor.execute("""SELECT {} from FREQUENCIES where idx='{}'""".format('ngram', word)).fetchall()[0][0]
        
        similarity = arr[1]
        frequencies = get_from_db(cursor=cursor, ngram=word, col=freq)

        d = {'ngrams':'{} ({})'.format(word, how_similar),\
             'frequencies':frequencies,
             'similarities':similarity}

        for el in d:
            res[el].append(d[el])

    return res


