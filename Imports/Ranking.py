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


# Loads the corpus information (document_id, url and tokens)
def load_corpusInformation():
    corpus_information_file = 'Tokenization/corpusInformation.txt'
    corpus_information = {}

    if os.path.isfile(corpus_information_file):
        with open(corpus_information_file, 'r') as ci_file:
            file_content = ci_file.read()
            corpus_information = json.loads(file_content)

    else:
        print("The corpus information file was not found. Please run the 'Tokenizer.py' file first.")

    return corpus_information
