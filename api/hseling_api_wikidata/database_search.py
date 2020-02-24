from itertools import groupby
import pandas as pd


class DatabaseSearch:
    
    def __init__(self, ngrams:list, morph, punct, cursor):
        
        self.morph = morph
        self.cursor = cursor
        self.punct = punct
        self.ngrams = ngrams
        self.lemmatized_ngrams = self.lemmatize()
        self.result = self.sql_query()
        self.csv_format = self.csv_format()
        
    def lemmatize(self):
        """ Returns lemmatized ngrams """
        lemmatized_ngrams = []
        ngrams = [n.split() for n in self.ngrams]
        for ngram in ngrams:
            if len(ngram) == 1:
                ngram = ngram[0].strip(self.punct).lower()
                ngram_lemma = ''.join(self.morph.lemmatize(ngram)).strip()
                lemmatized_ngrams.append(ngram_lemma)
            elif len(ngram) == 2:
                ngram = [w.strip(self.punct).lower() for w in ngram]
                ngram_lemma = ' '.join([' '.join(self.morph.lemmatize(w)).strip() for w in ngram])
                lemmatized_ngrams.append(ngram_lemma)
                
        return lemmatized_ngrams
        
    def sql_query(self):
        
        """Makes ngram queries to the ngram database"""
        
        ngrams_with_letters = {ngram: ngram[0] for ngram in self.lemmatized_ngrams}
        result = []

        for ngram, letter in ngrams_with_letters.items():
            self.cursor.execute(f"""SELECT * FROM ngrams WHERE 
                                    start_letter = '{letter}' 
                                    AND ngram = '{ngram}'""")
            result += self.cursor.fetchall()
            
        if result == []:
            raise NotFoundError("Ngrams not found")
            
        return result

    def csv_format(self):

        """ Converts the dictionaries with query result data into csv format (appropriate for downloading) """

        col_list = ["ngram", "start_letter", "Q_number",
                    "wiki_entity", "property_code", "property_value",
                    "object", "organization", "just_date",
                    "start_time", "end_time", "time_point",
                    "growth_speed", "google_year_1", "google_year_2", "id"]

        dict_format = [dict(zip(col_list, i)) for i in self.result]

        # add entry index
        for i, d in enumerate(dict_format):
            d["entry_id"] = i

        df = pd.DataFrame(dict_format, columns=["entry_id","ngram",
                    "wiki_entity", "Q_number", "property_code","property_value",
                     "object", "organization", "just_date",
                    "start_time","end_time","time_point",
                    "growth_speed","google_year_1","google_year_2"])

        csv_format = df.to_csv()

        return csv_format    

class NotFoundError(Exception):
    pass