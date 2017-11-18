import re

# Removes unwanted entries from tokenStream (mostly punctualtion)
def removeUnwantedEntries(tokenList):
    symbolEntry = re.compile("^[^a-zA-Z0-9]+$")

    return [x for x in tokenList if not symbolEntry.match(x)]


# Normalizes the tokenStream or Query terms
def normalizeList(tokenList):
    normalizedList = []
    symbolPattern = re.compile("[a-z]+[^a-zA-Z0-9_.-][a-z]+|^\W[a-z]+$|^[a-z]+\W$")
    possessivePattern = re.compile("^[a-z]+'s$")
    periodInitialsPattern = re.compile("^([a-z]\.){2,}$")

    for token in tokenList:
        # change to lower case
        token = token.lower()

        # removes symbols from words, except middle hyphens (ex: he/she = 1 token --> he she = 2 tokens)
        if symbolPattern.match(token):

            if possessivePattern.match(token):
                splittedTokens = re.findall(r'[a-z]+',token)
                normalizedList.append(splittedTokens[0])

            else:
                splittedTokens = re.findall(r'[a-z]+',token)
                normalizedList.extend(splittedTokens)

        else:
            if periodInitialsPattern.match(token):
                if token == 'u.s.':
                    token = 'usa'
                else:
                    splittedInitials = re.findall(r'[a-z]+',token)
                    token = ''.join(splittedInitials)

            normalizedList.append(token)

    return normalizedList


# Removes duplicates from tokenStream or Query
def removeDuplicates(tokenList):
    return list(set(tokenList))


# Processes the tokenStream
def processList(tokenList):
    cleanedUpList = []

    cleanedUpList = removeUnwantedEntries(tokenList)           # Removes non-word or number entries
    cleanedUpList = normalizeList(cleanedUpList)               # normalizes list
    unique_cleanedUpList = removeDuplicates(cleanedUpList)     # remove duplicates

    return cleanedUpList, unique_cleanedUpList


# Processes a Query
def processQuery(tokenList):
    cleanedUpList = []

    cleanedUpList = normalizeList(tokenList)            # normalizes list
    cleanedUpList = removeDuplicates(cleanedUpList)     # remove duplicates

    return cleanedUpList


# Processes an unfiltered tokenStream
def process_unfiltered_list(tokenList):
    unfilteredList = []

    unfilteredList = removeUnwantedEntries(tokenList)    # Removes non-word or number entries
    unfilteredList = removeDuplicates(unfilteredList)     # remove duplicates

    return unfilteredList
