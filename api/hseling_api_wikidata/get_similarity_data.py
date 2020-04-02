import json
import sqlite3
import os.path
import numpy as np
import pickle
import json
from dtaidistance import dtw
from numpy import dot
from numpy.linalg import norm

from sklearn.preprocessing import normalize

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(BASE_DIR + '/index2word.json', 'r') as f:
    index2word = json.loads(f.read())

with open(BASE_DIR + '/pos_dict.json', 'r') as f:
    pos_dict = json.loads(f.read())
    
index2word = {int(i):index2word[i] for i in index2word}
word2index = {index2word[w]:w for w in index2word}

rows = dict()

with open(BASE_DIR + "/rows_pct_change.pickle", "rb" ) as f:
    rows['pct'] = pickle.load(f)
    
with open(BASE_DIR + "/rows_rel.pickle", "rb" ) as f:
    rows['rel'] = pickle.load(f)

with open(BASE_DIR + '/total_count_dict1980.json', 'r') as f:
    totalcounts = np.array(list(json.loads(f.read()).values()))

# allowed = ('INTJ', 'ANUM', 'NUM', 'S', 'A', 'V')
#allowed = ('INTJ') #, 'A')
allowed = ('S', 'other')
not_allowed = ('CONJ', 'SPRO', 'PART', 'APRO', 'PR', 'ADVPRO', 'COM', 'ADV')
#allowed = ','.join(['"{}"'.format(i) for i in allowed])


def get_dtw(word, freq, n_words, window, years):
    y1, y2 = years
    
    arrays = rows[freq]
    # print(type(word2index[word]))
    
    vector1 = arrays[int(word2index[word])][y1:y2]
    
    dictionary = {}
    for w in word2index:
        idx = word2index[w]
        vector2 = arrays[int(idx)][y1:y2]
        dictionary[idx] = dtw.distance_fast(vector1, vector2, window)
    print('\n\n', word2index[word], '\n\n')
    for i in dictionary:
        print(i, dictionary[i])
        break
    dictionary = {w:dictionary[w] for w in dictionary if (pos_dict[index2word[w]] in allowed) or (w == word2index[word])}
    return sorted(dictionary.items(), key=lambda x:x[1], reverse=False)[:n_words]

def get_cosine(word, freq, n_words, years, window):
    y1, y2 = years
    
    years = list(range(y1, y2))
    M = normalize(rows[freq][:, years], axis=1)
    v1 = M[word2index[word]]
    # sims = dot(M, v1) / (M_norm * v1_norm)
    sims = M @ v1
    
    idxs = [w for w in np.argsort(sims)\
         if (pos_dict[index2word[w]] in allowed)\
              and (w != word2index[word])][::-1][:n_words]
    idxs = [word2index[word]] + idxs
    sims = sims[idxs]
    
    return list(zip(idxs, sims))

funcs = {'dtw':get_dtw, 'cosine':get_cosine}

def get_data(ngram, freq="rel",\
                sim="cosine",\
                n_words=30,\
                threshold=0.1,
                years=(1910, 1940),
                window=3):
    n = 0
    if sim == 'dtw':
        n = 1
    arrays = rows['rel']
    print(n_words)
    
    
    years_ = np.array(years) - 1880
    ngram = ngram.lower().strip()

    
    
    d = funcs[sim](ngram, freq=freq, window=window, n_words=n_words, years=years_)
    
    words, frequencies = [], []

    v = d[0][0]
    for i in d:
        idx = i[0]
        word = index2word[idx]
        similarity = i[1]
        freq_ = np.array(arrays[idx, years_[0]:years_[1]])

        freq_ = list(freq_ * totalcounts[years_[0]:years_[1]])
        
        frequencies.append(freq_)
        words.append('{} ({})'.format(word, round(n + (similarity * (-1)**n), ndigits=3)))
    
    res = {'ngrams':words, 'frequencies':frequencies, 'years':years}

    return res