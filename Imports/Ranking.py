import os
import json

# Loads the corpus statistics
def load_corpusStats():
    corpusStats_file = 'Tokenization/corpusStats.txt'
    corpusStats = {}

    if os.path.isfile(corpusStats_file):
        with open(corpusStats_file, 'r') as corpusStats_file:
            file_content = corpusStats_file.read()
            corpusStats = json.loads(file_content)

    else:
        print("The corpus statistics file was not found. Please run the 'Tokenizer.py' file first.")

    return corpusStats

# Loads the afinn_dictionary from file
def load_afinnSentiments():
    afinn_file = 'AFINN/afinnDictionary.txt'
    afinn_dictionary = {}

    if os.path.isfile(afinn_file):
        with open(afinn_file, 'r') as afinn_dictionary_file:
            file_content = afinn_dictionary_file.read()
            afinn_dictionary = json.loads(file_content)
    else:
        print("The afinnDictionary file was not found. Please run the 'Afinn_Dictionary.py' file first.")

    return afinn_dictionary


# Loads the documents sentiment
def load_documentsSentiment():
    documents_sentiment_file = 'Tokenization/documentsSentiment.txt'
    documents_sentiment = {}

    if os.path.isfile(documents_sentiment_file):
        with open(documents_sentiment_file, 'r') as ds_file:
            file_content = ds_file.read()
            documents_sentiment = json.loads(file_content)

    else:
        print("The documents sentiment file was not found. Please run the 'Tokenizer.py' file first.")
    
    return documents_sentiment
