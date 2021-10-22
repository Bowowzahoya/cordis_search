import re
import os
import shutil
import time

from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer, StemFilter, RegexTokenizer, LowercaseFilter, LanguageAnalyzer, SpaceSeparatedTokenizer
from whoosh import index
from whoosh import qparser
from whoosh.qparser import QueryParser

from .constants import *

def create_index(dataframe, index_directory=".whoosh_index/",
        id_column=ID_COL,
        text_columns=[TITLE_COL, OBJECTIVE_COL]):
    # create schema and directory
    
    regex_tokenizer = RegexTokenizer(expression=re.compile('\\w+(\\.?\\w+)*'), gaps=False)
    lower_case_filter = LowercaseFilter()
    stem_filter = StemFilter(lang='en', cachesize=50000)
    analyzer =  regex_tokenizer | lower_case_filter | stem_filter

    schema_dictionary = {id_column: TEXT(stored=True)}
    schema_dictionary.update({col: TEXT(stored=False, analyzer=analyzer) for col in text_columns})
    schema = Schema(**schema_dictionary)

    if not os.path.exists(index_directory):
        os.mkdir(index_directory)

    # fill index
    whoosh_index = index.create_in(index_directory, schema)
    writer = whoosh_index.writer()

    for i in range(len(dataframe)):
        row = dataframe.iloc[i]
        row_dictionary = {id_column: str(row[id_column])}
        row_dictionary.update({scol: str(row[col]) for scol, col in zip(text_columns, text_columns)})
        writer.add_document(**row_dictionary)
    writer.commit()

    return whoosh_index

def search_index(whoosh_index, query, search_fields=[TITLE_COL, OBJECTIVE_COL]):
    if not isinstance(query, str):
        return []

    schema = whoosh_index.schema
    search_fields = [col.replace(" ", "_") for col in search_fields] # whoosh indices can't have spaces
    parser = qparser.MultifieldParser(search_fields, schema)

    parsed_query = parser.parse(query)
    
    with whoosh_index.searcher() as s:
        results = s.search(parsed_query, limit=None)
        results_list = [list(res.fields().values())[0] for res in results]
        
    return results_list

def delete_index(index_directory=".whoosh_index/", sleep=1, retry=0, aftersleep=1):
    for _ in range(retry+1):
        time.sleep(sleep)
        try:
            shutil.rmtree(index_directory)
            break
        except:
            pass
    time.sleep(aftersleep)