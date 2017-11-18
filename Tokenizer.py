from Imports import TokenProcessing
from Imports import Ranking
import bs4 as bs
import nltk
import re
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

reuters_file_index = 0
reuters_base_fileName = 'Reuters-21578/reut2-0'
tokenStream = []
corpusStats = {
    'numOfDocs': 0,
    'docsLengths': {},
    'averageDocsLength' : 0
}
corpusLength = 0

# Loads the afinn_dictionary from file
afinn_sentiments = Ranking.load_afinnSentiments()
d_sentiment = 0
documents_sentiment = {}

for reuters_file_index in range(5):

    if reuters_file_index < 10:
        reuters_fileName = reuters_base_fileName + '0' + str(reuters_file_index) + '.sgm'
    else:
        reuters_fileName = reuters_base_fileName + str(reuters_file_index) + '.sgm'

    print("Processing '" + reuters_fileName + "' ...")

    with open(reuters_fileName, 'r', encoding='utf-8', errors='ignore') as file:
        file_content = file.read()
        soup = bs.BeautifulSoup(file_content, 'html.parser')

        for article in soup.find_all('reuters'):
            document_id = article.get('newid')
            title = article.title.text if article.title else ''
            body = article.body.text if article.body else ''


            titleTokens = nltk.word_tokenize(title)  # Tokenize the article's title
            bodyTokens = nltk.word_tokenize(body)    # Tokenize the article's body
            articleTokens = titleTokens + bodyTokens # join the title and body tokens

            # Processes the list (removes unwanted entries, normalizes the tokens (terms) and removes duplicates
            articleTokens, unique_articleTokens = TokenProcessing.processList(articleTokens)
            # articleTokens = TokenProcessing.process_unfiltered_list(articleTokens)  # Uncomment to get unfiltered tokenStream


            # Appends the article's tokens to the tokenStream
            for token in articleTokens:
                tokenStream.append([token, document_id])


            # Store corpus statistics
            corpusStats['numOfDocs'] += 1
            corpusStats['docsLengths'][document_id] = len(articleTokens)
            corpusLength += corpusStats['docsLengths'][document_id]


            # Generates document_sentiment
            for token in unique_articleTokens:
                if token in afinn_sentiments:
                    d_sentiment += int(afinn_sentiments[token])

            documents_sentiment[document_id] = d_sentiment
            # documents_sentiment[document_id] = d_sentiment / corpusStats['docsLengths'][document_id]        # normalized sentiment
            d_sentiment = 0


    # increments file index
    reuters_file_index += 1



# Calculate average document length
corpusStats['averageDocsLength'] = corpusLength / corpusStats['numOfDocs']


tokenStream_fileName = 'Tokenization/tokenStream.txt'
# tokenStream_fileName = 'Tokenization/unfiltered_tokenStream.txt'    # Uncomment to get unfiltered tokenStream

corpusStats_fileName = 'Tokenization/corpusStats.txt'
documents_sentiment_fileName = 'Tokenization/documentsSentiment.txt'


# Save tokenStream to file
write_to_file(tokenStream, tokenStream_fileName)
print("Token stream successfully saved to '" + tokenStream_fileName + "' file.")


# Save corpusStats to file (number of documents, document lengths and avg document length)
write_to_file(corpusStats, corpusStats_fileName)
print("Corpus statistics successfully saved to '" + corpusStats_fileName + "' file.")

# Save documents_sentiment to file (number of documents, document lengths and avg document length)
write_to_file(documents_sentiment, documents_sentiment_fileName)
print("Documents sentiment successfully saved to '" + documents_sentiment_fileName + "' file.")
