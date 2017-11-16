from Imports import TokenProcessing
import os
import json
import math

# Calculates the RSV_result in order to rank the results
def calculate_RSV(SPIMI_dictionary, corpusStats, term, docID):
    document_frequency = SPIMI_dictionary[term]['df']
    term_frequency = SPIMI_dictionary[term]['docs'][str(docID)]['tf']
    num_of_docs = int(corpusStats['numOfDocs'])
    document_length = int(corpusStats['docsLengths'][str(docID)])
    average_docs_length = float(corpusStats['averageDocsLength'])
    k_parameter = 1.5
    b_parameter = 0.5

    # Okapi BM25 formula
    RSV_result = math.log(num_of_docs / document_frequency) * (((k_parameter + 1) * term_frequency) / (k_parameter * ((1 - b_parameter) + b_parameter * (document_length / average_docs_length)) + term_frequency))

    return RSV_result


# Searches with AND operator
def search_with_AND(terms, SPIMI_dictionary):
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
def search_with_OR(terms, SPIMI_dictionary, corpusStats):
    docs_and_RSV = {}
    result = []

    for term in terms:
        if term in SPIMI_dictionary:
            term_Docs = list(map(int, SPIMI_dictionary[term]['docs'].keys()))

            for docID in term_Docs:

                RSV_result = calculate_RSV(SPIMI_dictionary, corpusStats, term, docID)

                if docID in docs_and_RSV:
                    docs_and_RSV[docID] += RSV_result
                else:
                    docs_and_RSV[docID] = RSV_result


    # Line of code from https://stackoverflow.com/questions/9919342/sorting-a-dictionary-by-value-then-key
    result = [value for value in sorted(docs_and_RSV.items(), key=lambda kv: (-kv[1], kv[0]))]
    totalCount = len(result)

    if totalCount > 0:
        print('Total number of results found: ' + str(totalCount))
        print('Documents: ' + str(result) + '\n')

    else:
        print('No results were found.\n')


# Determines whether to use AND or OR operator
def search_inverted_index(query, SPIMI_dictionary, corpusStats):

    # many terms with AND operator '&'
    if '&' in query:
        terms = query.split('&')

        # Processes the list (removes unwanted entries, normalizes the tokens (terms) and removes duplicates
        terms = TokenProcessing.processQuery(terms)

        search_with_AND(terms, SPIMI_dictionary)


    # one or many terms with OR operator ' ' (space)
    else:
        terms = query.split(' ')

        # Processes the list (removes unwanted entries, normalizes the tokens (terms) and removes duplicates
        terms = TokenProcessing.processQuery(terms)

        search_with_OR(terms, SPIMI_dictionary, corpusStats)



# Execution starts here
SPIMI_file_name = 'SPIMI/SPIMI_dictionary.txt'
corpusStats_file_name = 'Tokenization/corpusStats.txt'

SPIMI_dictionary = {}
corpusStats = {}

# Load SPIMI dictionary
if os.path.isfile(SPIMI_file_name):
    with open(SPIMI_file_name, 'r') as SPIMI_file:
        file_content = SPIMI_file.read()
        SPIMI_dictionary = json.loads(file_content)

else:
    print("The SPIMI dictionary file was not found. Please run the 'SPIMI.py' file first.")


# Load corpus statistics
if os.path.isfile(corpusStats_file_name):
    with open(corpusStats_file_name, 'r') as corpusStats_file:
        file_content = corpusStats_file.read()
        corpusStats = json.loads(file_content)

else:
    print("The corpus statistics file was not found. Please run the 'Tokenizer.py' file first.")


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

    search_inverted_index(query, SPIMI_dictionary, corpusStats)

    continueScript = input('Would you like to enter another query (y/n): ')
    print('\n')
