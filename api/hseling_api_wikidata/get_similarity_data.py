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
    print(col)
    res = json.loads(res[0][0])
    print('\n\nres:', res, '\n\n')
    if type(res) == dict:
        res = [list(i) for i in sorted(res.items(), key=lambda x:x[1], reverse=True)]
    return res


def get_data(ngram, freq="rel", sim="cosine"):
    sim = "top_{}_{}".format(sim, freq)
    freq = "rows_" + freq
    # print(sim)
    #print(freq)
     
    path_to_db = os.path.join(BASE_DIR, "ngrams.db")
    cursor = connect_to_db(path_to_db)
    # if pct_change:
    #     freq, sim = 'change_rates', 'top10_cosine_change_rate'
    # else:
    #     freq, sim = 'relative_frequencies_1918_2009', 'top10_cosine_rel_values'
    
    sims = get_from_db(cursor=cursor, ngram=ngram.lower(), col=sim)

    # print('\n\n', sims, '\n\n')
    res = {'ngrams':[], 'frequencies':[], 'similarities':[]}
    for arr in sims:
        
        word = arr[0]
        print('\n\n', word, '\n\n')
        word = cursor.execute("""SELECT {} from FREQUENCIES where idx='{}'""".format('ngram', word)).fetchall()[0][0]
        
        similarity = arr[1]
        frequencies = get_from_db(cursor=cursor, ngram=word, col=freq)

        d = {'ngrams':word,\
             'frequencies':frequencies,
             'similarities':similarity}

        for el in d:
            res[el].append(d[el])

    return res


