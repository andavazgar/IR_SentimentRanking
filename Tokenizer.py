from Imports import TokenProcessing
import nltk
import os
import json

# Writes data to a file
def write_to_file(dataObject, fileName):

    fileName = fileName if '/' in fileName else './' + fileName

    dirName = os.path.dirname(fileName)

    if not os.path.exists(dirName):
        os.makedirs(dirName)

    with open(fileName, 'w') as output_file:
        output_file.write(json.dumps(dataObject, indent=2))


# Execution starts here
nltk.data.path.append("./nltk/nltk_data")


corpus_directory = 'Corpus/'                    # Path of the corpus documents
corpus_files = os.listdir(corpus_directory)     # List of documents to tokenize (corpus)
file_processing_counter = 0                     # Counter (total number of documents that have been processed / tokenized)
total_num_corpus_files = len(corpus_files)      # Total number of files to tokenize
corpus_information = []                         # Contains the url and tokens for each document in the corpus

tokenStream = []
corpusStats = {
    'numOfDocs': 0,
    'docsLengths': {},
    'averageDocsLength' : 0
}
corpusLength = 0


print('Processing...', end='\r')

for fname in corpus_files:

    # Skips files that are not .txt
    if not fname.endswith('.txt'):
        continue

    file_processing_counter += 1

    document_id = len(corpus_information)
    formatted_url = fname.replace('_', '.').replace('--', '/')[:-4]     # Converts the filename to url
    document_info = {}

    document_info['url'] = formatted_url

    file_name = corpus_directory + fname

    print('Tokenizing file number: ' + str(file_processing_counter) + ' of ' + str(total_num_corpus_files), end='\r')

    with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
        document_text = file.read()
        document_tokens = nltk.word_tokenize(document_text)    # Tokenize the document text

        # Processes the list (removes unwanted entries, normalizes the tokens (terms)
        document_tokens = TokenProcessing.processList(document_tokens)
        # document_tokens = TokenProcessing.process_unfiltered_list(document_tokens)  # Uncomment to get unfiltered tokenStream

        document_info['tokens'] = document_tokens
        corpus_information.append(document_info)    # Adds the document_info (url and tokens) the the corpus_information


        # Appends the document's tokens to the tokenStream
        for token in document_tokens:
            tokenStream.append([token, document_id])


        # Store corpus statistics
        corpusStats['numOfDocs'] += 1
        corpusStats['docsLengths'][document_id] = len(document_tokens)
        corpusLength += corpusStats['docsLengths'][document_id]



# Calculate average document length
corpusStats['averageDocsLength'] = corpusLength / corpusStats['numOfDocs']


tokenStream_fileName = 'Tokenization/tokenStream.txt'
# tokenStream_fileName = 'Tokenization/unfiltered_tokenStream.txt'    # Uncomment to get unfiltered tokenStream

corpusStats_fileName = 'Tokenization/corpusStats.txt'
corpus_information_fileName = 'Tokenization/corpusInformation.txt'


# Save tokenStream to file
write_to_file(tokenStream, tokenStream_fileName)
print("Token stream successfully saved to '" + tokenStream_fileName + "' file.")


# Save corpusStats to file (number of documents, document lengths and avg document length)
write_to_file(corpusStats, corpusStats_fileName)
print("Corpus statistics successfully saved to '" + corpusStats_fileName + "' file.")

# Save corpus_information to file (document_id, url and tokens). Used in Query.py
write_to_file(corpus_information, corpus_information_fileName)
print("Corpus information successfully saved to '" + corpus_information_fileName + "' file.")
