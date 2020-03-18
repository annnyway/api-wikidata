import json
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def connect_to_db(path_to_db):
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    return cursor

def get_from_db(cursor, word, col):

    res = cursor.execute("""SELECT {} from FREQUENCIES where ngram='{}'""".format(col, word)).fetchall()
    res = json.loads(res[0][0])
    if type(res) == dict:
        res = [list(i) for i in sorted(res.items(), key=lambda x:x[1], reverse=True)]
    return res


def get_data(word, pct_change=False):
    path_to_db = os.path.join(BASE_DIR, "ngrams.db")
    if pct_change:
        freq, sim = 'change_rates', 'top10_cosine_change_rate'
    else:
        freq, sim = 'relative_frequencies_1918_2009', 'top10_cosine_rel_values'

    cursor = connect_to_db(path_to_db)
    sims = get_from_db(cursor, word, sim)

    res = {'ngrams':[], 'frequencies':[], 'similarities':[]}
    for arr in sims:


        ngram = arr[0]

        similarity = arr[1]
        frequencies = get_from_db(cursor, ngram, freq)

        d = {'ngrams':ngram,\
             'frequencies':frequencies,
             'similarities':similarity}

        for el in d:
            res[el].append(d[el])

    return res


