import matplotlib.pyplot as plt
import json

class DatabaseSearch:
    
    def __init__(self, ngrams:list, morph, punct, cursor):
        self.morph = morph
        self.cursor = cursor
        self.punct = punct
        self.ngrams = ngrams
        self.lemmatized_ngrams = self.lemmatize()
        self.sql_result = self.sql_query()
        self.coordinates = self.get_coordinates()
        
        
    def lemmatize(self):
        """Returns lemmatized ngrams"""
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
            #    raise IndexError("Вы ввели одну или несколько биграмм. Поиск по биграммам пока не поддерживается. Пожалуйста, удалите биграммы из запроса и повторите поиск")
            # elif len(ngram) >= 3:
            #    raise IndexError("Вы ввели одну или несколько триграмм. Поиск по триграммам и более длинным сочетаниям слов пока не поддерживается. Пожалуйста, удалите их из запроса и повторите поиск")
        return lemmatized_ngrams
        
        
    def sql_query(self):
        """Looks for the query ngrams in the database 
        and returns a list of dictionaries, 
        where one dictionary is an entry from the database"""
        
        ngrams_with_letters = {ngram: ngram[0] for ngram in self.lemmatized_ngrams}
        result = []

        for ngram, letter in ngrams_with_letters.items():
            self.cursor.execute(f"""SELECT * FROM ngrams WHERE 
                                    start_letter = '{letter}' 
                                    AND ngram = '{ngram}'""")
            result += self.cursor.fetchall()
            
        if result == []:
            raise NotFoundError("Ngrams not found")
        col_list = ["ngram", "start_letter", "Q_number", 
                    "wiki_entity", "property_code","property_value",
                     "object", "organization", "just_date",
                    "start_time","end_time","time_point",
                    "growth_speed","google_year_1","google_year_2", "id"]
        
        sql_dict = [dict(zip(col_list,i)) for i in result]
        
        # add entry index
        for i,d in enumerate(sql_dict):
            d["entry_id"] = i 
            
        return sql_dict
        
    
    def get_coordinates(self):
        """Returns a sorted list of triples:
        (entry id in database search result, year, growth speed value)"""
        coords = []
        for d in self.sql_result:
            coords.append((d["entry_id"], d["google_year_1"], d["growth_speed"]))
            if d["google_year_2"]:
                coords.append((d["entry_id"], d["google_year_2"], d["growth_speed"]))  
        sorted_coords = sorted(coords, key=self.getKey)
        return sorted_coords
    
    
    @staticmethod
    def getKey(item):
        """Returns keys for sorting coordinates by years"""
        return item[1]
        
        
    def get_plot(self):
        """Draws a plot:
        x - ngrams' years of interest found in Wikidata;
        y - frequency growth speed value standardized by removing the mean 
        and scaling to unit variance whithin every ngram sample;
        point labels - ngram index in the batabase output"""
        x = [i[1] for i in self.coordinates]
        y = [i[2] for i in self.coordinates]
        plt.figure(figsize=(13, 8))
        plt.plot(x,y)
        for coord in self.coordinates:
            plt.annotate(coord[0],(coord[1],coord[2]))
        plt.show()


class NotFoundError(Exception):
    pass