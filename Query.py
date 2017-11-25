from Imports import TokenProcessing
from Imports import Ranking
import os
import json
import math
import sys

# Calculates the ranking_score based on the Okapi BM25 formula
def calculate_RSV(term, docID):
    global SPIMI_dictionary
    global corpusStats

    document_frequency = SPIMI_dictionary[term]['df']
    term_frequency = SPIMI_dictionary[term]['docs'][str(docID)]['tf']
    num_of_docs = int(corpusStats['numOfDocs'])
    document_length = int(corpusStats['docsLengths'][str(docID)])
    average_docs_length = float(corpusStats['averageDocsLength'])
    k_parameter = 1.5
    b_parameter = 0.5

    # Okapi BM25 formula
    ranking_score = math.log(num_of_docs / document_frequency) * (((k_parameter + 1) * term_frequency) / (k_parameter * ((1 - b_parameter) + b_parameter * (document_length / average_docs_length)) + term_frequency))

    return ranking_score


def calculate_document_sentiment(docID):
    global SPIMI_dictionary
    global corpusStats
    global corpus_information

    d_sentiment = 0

    # Generates document_sentiment
    for token in corpus_information[docID]['tokens']:
        d_sentiment += int(SPIMI_dictionary[token]['sentiment'])

    return d_sentiment / corpusStats['docsLengths'][str(docID)]

# Retrieves the sentiment for the given term
def get_term_sentiment(term):
    global SPIMI_dictionary

    return SPIMI_dictionary[term]['sentiment']


# Searches with AND operator
def search_with_AND(terms):
    global SPIMI_dictionary

    terms_df = {}
    terms_search_order = []
    result = []

    # Builds dictionary with term --> document_frequency
    for term in terms:
        if term in SPIMI_dictionary:
            terms_df[term] = SPIMI_dictionary[term]['df']
        elif term != '':
            terms_df = []
            break

    # Builds a list of terms sorted by ascending document_frequency
    terms_search_order = sorted(terms_df, key=terms_df.__getitem__)

    search_order_length = len(terms_search_order)
    search_order_index = 1

    if search_order_length > 0:
        result = list(map(int, SPIMI_dictionary[terms_search_order[0]]['docs'].keys()))

    while search_order_index < search_order_length:
        result = list(set(result) & set(list(map(int, SPIMI_dictionary[terms_search_order[search_order_index]]['docs'].keys()))))
        search_order_index += 1


    result = sorted(result)
    totalCount = len(result)

    if totalCount > 0:
        print('Total number of results found: ' + str(totalCount))
        print('Documents: ' + str(result) + '\n')

    else:
        print('No results were found.\n')


# Searches with OR operator
def search_with_OR(terms):
    global SPIMI_dictionary
    global ranking_options
    global ranking_method
    global corpusStats

    term_Docs = []
    docs_and_ranking = {}
    result = []
    high_to_low_ranking = True

    if ranking_method == 'bm25':
        for term in terms:
            if term in SPIMI_dictionary:
                term_Docs = list(map(int, SPIMI_dictionary[term]['docs'].keys()))

            for docID in term_Docs:
                ranking_score = calculate_RSV(term, docID, corpusStats)
                url = corpus_information[docID]['url']

                if docID in docs_and_ranking:
                    docs_and_ranking[url] += ranking_score
                else:
                    docs_and_ranking[url] = ranking_score


    elif ranking_method == 'sentiment':
        corpus_information = Ranking.load_corpusInformation()
        query_sentiment = 0

        for term in terms:
            if term in SPIMI_dictionary:
                term_Docs = list(map(int, SPIMI_dictionary[term]['docs'].keys()))

                ranking_score = get_term_sentiment(term)
                query_sentiment += ranking_score

                for docID in term_Docs:
                    url = corpus_information[docID]['url']
                    docs_and_ranking[url] = calculate_document_sentiment(docID)

        if query_sentiment < 0:
            high_to_low_ranking = False


    else:
        print('An invalid ranking method was chosen (\'' + ranking_method + '\'). Please change the ranking method to one of the following: ' + str(ranking_options) + '.')
        sys.exit()


    if high_to_low_ranking:
        result = [value for value in sorted(docs_and_ranking.items(), key=lambda kv: (-kv[1], kv[0]))]

    else:
        result = [value for value in sorted(docs_and_ranking.items(), key=lambda kv: (kv[1], kv[0]))]


    totalCount = len(result)

    if totalCount > 0:
        print('Total number of results found: ' + str(totalCount))
        print('Documents: ')

        for doc_ranking in result:
            print(doc_ranking)

        print()

    else:
        print('No results were found.\n')


# Determines whether to use AND or OR operator
def search_inverted_index(query):

    # many terms with AND operator '&'
    if '&' in query:
        terms = query.split('&')

        # Processes the list (removes unwanted entries, normalizes the tokens (terms) and removes duplicates
        terms = TokenProcessing.processQuery(terms)

        search_with_AND(terms)


    # one or many terms with OR operator ' ' (space)
    else:
        terms = query.split(' ')

        # Processes the list (removes unwanted entries, normalizes the tokens (terms) and removes duplicates
        terms = TokenProcessing.processQuery(terms)

        search_with_OR(terms)



# Execution starts here
SPIMI_file_name = 'SPIMI/SPIMI_dictionary.txt'
SPIMI_dictionary = {}

#                    0          1
ranking_options = ['bm25', 'sentiment']
ranking_method = ranking_options[1]

corpusStats = Ranking.load_corpusStats()                # Loads the corpusStats (number of documents, document lengths and avg document length)
corpus_information = Ranking.load_corpusInformation()   # Loads the corpus_information (document url and tokens)

# Loads the SPIMI dictionary
if os.path.isfile(SPIMI_file_name):
    with open(SPIMI_file_name, 'r') as SPIMI_file:
        file_content = SPIMI_file.read()
        SPIMI_dictionary = json.loads(file_content)

else:
    print("The SPIMI dictionary file was not found. Please run the 'SPIMI.py' file first.")


print('''
/*********************************************************
*                                                        *
*       Query instructions:                              *
*       AND operator: separate terms with &              *
*       OR operator: separate terms with a space         *
*                                                        *
*********************************************************/

''')

continueScript = 'y'

while continueScript and continueScript[0] == 'y':
    query = input('Please enter a query: ')

    search_inverted_index(query)

    continueScript = input('Would you like to enter another query (y/n): ')
    print('\n')
