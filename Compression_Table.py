import re
import os
import json

# Prints the table's headings
def print_table_headings(col_lengths):
    headings = ['', 'Word Types (terms)', 'Non-positional postings']
    sub_headings = ['Size of', 'dictionary', 'Non-positional index']
    sub_headings2 = ['Size', 'Δ', 'cml']
    col_index = 0

    print('|', end='')
    for heading in headings:
        print(' '*((col_lengths[col_index] - len(heading))//2) + heading + ' '*(((col_lengths[col_index] - len(heading))//2) + (col_lengths[col_index] - len(heading)) % 2) + '|', end='')
        col_index += 1
    print()


    col_index = 0

    print('|', end='')
    for sub_heading in sub_headings:
        print(' '*((col_lengths[col_index] - len(sub_heading))//2) + sub_heading + ' '*(((col_lengths[col_index] - len(sub_heading))//2) + (col_lengths[col_index] - len(sub_heading)) % 2) + '|', end='')
        col_index += 1
    print()


    col_index = 1
    num_of_columns = len(col_lengths)

    print('|' + ' '*(col_lengths[0]) + '|', end='')
    while col_index < num_of_columns:
        print(' '*((col_lengths[col_index] - len(sub_headings2[0]) - 8)//2) + sub_headings2[0] + ' '*(((col_lengths[col_index] - len(sub_headings2[0]) - 8)//2) + (col_lengths[col_index] - len(sub_headings2[0])) % 2), end='')
        print('  ' + sub_headings2[1] + ' ' + sub_headings2[2] + ' |', end='')
        col_index += 1
    print()


# Prints the table's body
def print_table_body():
    for testName, testValues in compression_table.items():
        # Start of table line
        print('|', end='')

        # Test Name
        if 'test_name' in testValues:
            print(' ' + testValues['test_name'] + ' '*((col_lengths[0] - len(testValues['test_name']) - 1)) + '|', end='')

        else:
            print_empty_tableCell(col_lengths[0])

        # Dictionary totals
        if 'total_dictionary_size' in testValues:
            total_value = "{:,}".format(testValues['total_dictionary_size'])
            total_value_length = len(total_value)

            # Dictionary total
            print(' ' + total_value + ' '*(col_lengths[1] - total_value_length - 9), end='')


            if testName == 'unfilteredd':
                    print(' '*(8), end='')

            else:
                # Delta dictionary total
                if 'delta_dictionary' in testValues:
                    delta_value = formatNumber(testValues['delta_dictionary'])
                    print(delta_value + ' ', end='')

                else:
                    print(' '*(4), end='')


                # Cml dictionary total
                if 'cml_dictionary' in testValues:
                    cml_value = formatNumber(testValues['cml_dictionary'])
                    print(cml_value + ' |', end='')

                else:
                    print(' '*(4) + '|', end='')

        else:
            print_empty_tableCell(col_lengths[1])


        # Postings totals
        if 'total_postings' in testValues:
            total_value = "{:,}".format(testValues['total_postings'])
            total_value_length = len(total_value)

            
            # Postings total
            print(' ' + total_value + ' '*(col_lengths[2] - total_value_length - 9), end='')


            if testName == 'unfilteredd':
                    print(' '*(8), end='')

            else:
                # Delta postings total
                if 'delta_postings' in testValues:
                    delta_value = formatNumber(testValues['delta_postings'])
                    print(delta_value + ' ', end='')

                else:
                    print(' '*(4), end='')


                # Cml postings total
                if 'cml_postings' in testValues:
                    cml_value = formatNumber(testValues['cml_postings'])
                    print(cml_value + ' |', end='')

                else:
                    print(' '*(4) + '|', end='')

        else:
            print_empty_tableCell(col_lengths[2])

        # end of table line
        print()


# Prints an empty table cell
def print_empty_tableCell(length):
    print(' '*(length) + '|', end='')


# Prints an empty table line
def print_empty_tableLine(col_lengths):
    col_index = 0
    num_of_columns = len(col_lengths)

    print('|', end='')
    while col_index < num_of_columns:
        print(' '*(col_lengths[col_index]) + '|', end='')
        col_index += 1
    print()


# Prints a horizontal line (for separation)
def print_horizontal_tableLine(col_lengths, isTop=False):
    col_index = 0
    num_of_columns = len(col_lengths)
    col_dividor_symbol = '|'

    if isTop:
        col_dividor_symbol = '_'

    print(col_dividor_symbol, end='')
    while col_index < num_of_columns:
        print('_'*(col_lengths[col_index]) + col_dividor_symbol, end='')
        col_index += 1
    print()


# Formats percentages of compression
def formatNumber(number):
    returnedValue = ''

    if abs(number) < 10:
        returnedValue = ' -' + str(abs(number))
    else:
        returnedValue = '-' + str(abs(number))

    return returnedValue


# Gets the length the of the dictionary
def getTotal_dictionary(SPIMI_dictionary):
    return len(SPIMI_dictionary)


# Gets the length of all the postings lists. It adds all the documents frequencies.
def getTotal_postings(SPIMI_dictionary):
    totalPostings = 0

    for term in SPIMI_dictionary:
        totalPostings += SPIMI_dictionary[term]['df']

    return totalPostings


# It calculates the cumulative compression change
def getCumulative(currentTestValue, prevTestValue):
    return int(round(((prevTestValue - currentTestValue) / prevTestValue) * 100))


# Removes numbers from the inverted index
def noNumbers(unfiltered_SPIMI_dictionary):
    numberPattern = re.compile("[0-9]+")
    noNumbers_dictionary = {}

    for term in unfiltered_SPIMI_dictionary:
        if not numberPattern.match(term):
            noNumbers_dictionary[term] = unfiltered_SPIMI_dictionary[term]

    return noNumbers_dictionary


# Case folds the inverted index
def caseFolding(noNumbers_dictionary):
    caseFolding_dictionary = {}

    for term in noNumbers_dictionary:
        lowercase_term = term.lower()

        if lowercase_term in caseFolding_dictionary:
            new_posting_list = []
            new_posting_list = list(set(caseFolding_dictionary[lowercase_term]['docs']) | set(noNumbers_dictionary[term]['docs']))
            new_posting_list = sorted(new_posting_list)
            caseFolding_dictionary[lowercase_term]['df'] = len(new_posting_list)
            caseFolding_dictionary[lowercase_term]['docs'] = new_posting_list
        else:
            caseFolding_dictionary[lowercase_term] = noNumbers_dictionary[term]

    return caseFolding_dictionary


# Removes the stop words from the inverted index
def stopWords_removal(caseFolding_dictionary, stopWords_list):
    stopWords_dictionary = {}

    for term in caseFolding_dictionary:
        if term not in stopWords_list:
            stopWords_dictionary[term] = caseFolding_dictionary[term]

    return stopWords_dictionary


# Removes 30 stop words
def stopWords_30(caseFolding_dictionary):
    # Stop words taken from the slides. Chapter 2 (32/62)
    stopWords_30_list = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he", "his", "i", "in",
    "is", "it", "its", "of", "on", "she", "that", "the", "to", "was", "we", "were", "will", "with", "you"]

    return stopWords_removal(caseFolding_dictionary, stopWords_30_list)


# Removes 150 stop words
def stopWords_150(caseFolding_dictionary):
    # Stop words taken from https://www.ranks.nl/stopwords
    stopWords_150_list = ["a", "about", "above", "after", "again", "against", "all", "almost", "also", "always", "am",
    "an", "and", "any", "anyone", "are", "around", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can't", "could", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
    "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he's", "her", "here",
    "hers", "herself", "him", "himself", "his", "how", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",
    "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mostly", "much", "my", "myself", "never",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "out", "over", "own", "same",
    "she", "should", "so", "some", "someone", "something",  "such", "than", "that", "that's", "the", "their", "them",
    "then", "there", "there's", "these", "they", "they're", "they've", "this", "those", "through", "to", "together",
    "too", "under", "until", "up", "us", "very", "was", "wasn't", "we", "we'd", "we're", "we've", "well", "were", "what",
    "what's", "when","where", "which", "while", "who", "why", "will", "with", "would", "you", "yourself"]

    return stopWords_removal(caseFolding_dictionary, stopWords_150_list)


# Populates the table data
def populate_compressionTable_data(test_name, total_dictionary_size, delta_dictionary, cml_dictionary, total_postings, delta_postings, cml_postings):
    compression_table[test_name]['total_dictionary_size'] = total_dictionary_size
    compression_table[test_name]['delta_dictionary'] = delta_dictionary
    compression_table[test_name]['cml_dictionary'] = cml_dictionary
    compression_table[test_name]['total_postings'] = total_postings
    compression_table[test_name]['delta_postings'] = delta_postings
    compression_table[test_name]['cml_postings'] = cml_postings


# Prints the table
def print_compression_table():
    print_horizontal_tableLine(col_lengths, True)
    print_empty_tableLine(col_lengths)
    print_table_headings(col_lengths)
    print_horizontal_tableLine(col_lengths)
    print_table_body()
    print_horizontal_tableLine(col_lengths)


# Execution starts here
compression_table = {
    'unfiltered': {'test_name': 'Unfiltered'},
    'noNumbers': {'test_name': 'No numbers'},
    'caseFolding': {'test_name': 'Case folding'},
    'stopWords_30': {'test_name': '30 Stop words'},
    'stopWords_150': {'test_name': '150 Stop words'}
}

# Column widths
col_lengths = [16, 20, 25]

SPIMI_file_name = 'SPIMI/Unfiltered_SPIMI/unfiltered_SPIMI_dictionary.txt'

if os.path.isfile(SPIMI_file_name):
    with open(SPIMI_file_name, 'r') as SPIMI_file:
        file_content = SPIMI_file.read()
        unfiltered_SPIMI_dictionary = json.loads(file_content)

        unfiltered_totalDictionary = getTotal_dictionary(unfiltered_SPIMI_dictionary)
        unfiltered_totalPostings = getTotal_postings(unfiltered_SPIMI_dictionary)

        populate_compressionTable_data('unfiltered', unfiltered_totalDictionary, 0, 0, unfiltered_totalPostings, 0, 0)


        # No numbers
        noNumbers_dictionary = noNumbers(unfiltered_SPIMI_dictionary)

        noNumbers_totalDictionary = getTotal_dictionary(noNumbers_dictionary)
        noNumbers_cml_dictionary = getCumulative(noNumbers_totalDictionary, compression_table['unfiltered']['total_dictionary_size'])
        noNumbers_delta_dictionary = noNumbers_cml_dictionary - compression_table['unfiltered']['cml_dictionary']

        noNumbers_totalPostings = getTotal_postings(noNumbers_dictionary)
        noNumbers_cml_postings = getCumulative(noNumbers_totalPostings, compression_table['unfiltered']['total_postings'])
        noNumbers_delta_postings = noNumbers_cml_postings - compression_table['unfiltered']['cml_postings']

        populate_compressionTable_data('noNumbers', noNumbers_totalDictionary, noNumbers_delta_dictionary, noNumbers_cml_dictionary, noNumbers_totalPostings, noNumbers_delta_postings, noNumbers_cml_postings)


        # Case folding
        caseFolding_dictionary = caseFolding(noNumbers_dictionary)

        caseFolding_totalDictionary = getTotal_dictionary(caseFolding_dictionary)
        caseFolding_cml_dictionary = getCumulative(caseFolding_totalDictionary, compression_table['unfiltered']['total_dictionary_size'])
        caseFolding_delta_dictionary = caseFolding_cml_dictionary - compression_table['noNumbers']['cml_dictionary']

        caseFolding_totalPostings = getTotal_postings(caseFolding_dictionary)
        caseFolding_cml_postings = getCumulative(caseFolding_totalPostings, compression_table['unfiltered']['total_postings'])
        caseFolding_delta_postings = caseFolding_cml_postings - compression_table['noNumbers']['cml_postings']

        populate_compressionTable_data('caseFolding', caseFolding_totalDictionary, caseFolding_delta_dictionary, caseFolding_cml_dictionary, caseFolding_totalPostings, caseFolding_delta_postings, caseFolding_cml_postings)


        # 30 Stop words
        stopWords_30_dictionary = stopWords_30(caseFolding_dictionary)

        stopWords_30_totalDictionary = getTotal_dictionary(stopWords_30_dictionary)
        stopWords_30_cml_dictionary = getCumulative(stopWords_30_totalDictionary, compression_table['unfiltered']['total_dictionary_size'])
        stopWords_30_delta_dictionary = stopWords_30_cml_dictionary - compression_table['caseFolding']['cml_dictionary']

        stopWords_30_totalPostings = getTotal_postings(stopWords_30_dictionary)
        stopWords_30_cml_postings = getCumulative(stopWords_30_totalPostings, compression_table['unfiltered']['total_postings'])
        stopWords_30_delta_postings = stopWords_30_cml_postings - compression_table['caseFolding']['cml_postings']

        populate_compressionTable_data('stopWords_30', stopWords_30_totalDictionary, stopWords_30_delta_dictionary, stopWords_30_cml_dictionary, stopWords_30_totalPostings, stopWords_30_delta_postings, stopWords_30_cml_postings)


        # 150 Stop words
        stopWords_150_dictionary = stopWords_150(caseFolding_dictionary)

        stopWords_150_totalDictionary = getTotal_dictionary(stopWords_150_dictionary)
        stopWords_150_cml_dictionary = getCumulative(stopWords_150_totalDictionary, compression_table['unfiltered']['total_dictionary_size'])
        stopWords_150_delta_dictionary = stopWords_150_cml_dictionary - compression_table['caseFolding']['cml_dictionary']

        stopWords_150_totalPostings = getTotal_postings(stopWords_150_dictionary)
        stopWords_150_cml_postings = getCumulative(stopWords_150_totalPostings, compression_table['unfiltered']['total_postings'])
        stopWords_150_delta_postings = stopWords_150_cml_postings - compression_table['caseFolding']['cml_postings']

        populate_compressionTable_data('stopWords_150', stopWords_150_totalDictionary, stopWords_150_delta_dictionary, stopWords_150_cml_dictionary, stopWords_150_totalPostings, stopWords_150_delta_postings, stopWords_150_cml_postings)



    print_compression_table()
    print()

else:
    print("The unfiltered SPIMI dictionary file was not found. Please run the 'SPIMI.py' file first.")
    print("Remember to uncomment the unfiltered lines on the 'Tokenizer.py' and 'SPIMI.py'.")
