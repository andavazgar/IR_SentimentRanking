import sys
import os
import json

# Returns the Token from tokenStream entry
def getToken(tokenEntry):
    return tokenEntry[0]


# Returns the DocID from tokenStream entry
def getDocID(tokenEntry):
    return int(tokenEntry[1])


# Deletes the previously created blocks from the directory
def cleanDirectory(path):
    fileList = os.listdir(path)

    for f in fileList:
        if os.path.isfile(os.path.join(path, f)):
            os.remove(os.path.join(path, f))

    print("Directory cleaned.")


# Writes a block on disk (mini inverted index)
def write_dict_to_file(fileBaseName, fileIndex, block_dictionary):
    fileName = fileBaseName + str(fileIndex) + '.txt'
    dirName = os.path.dirname(fileName)

    if not os.path.exists(dirName):
        os.makedirs(dirName)

    with open(fileName, 'w') as blockFile:
        blockFile.write(json.dumps(block_dictionary, indent=2, sort_keys=True))

        print("Block dictionary successfully saved to '" + fileName + "' file.")


# Processes the tokenStream and generates the inverted index
def SPIMI_Invert(tokenStream, fileBaseName):
    fileIndex = 0
    blockSizeLimit = 1     # Max size of block in MB
    block_dictionary = {}

    for tokenEntry in tokenStream:
        if (sys.getsizeof(block_dictionary)/1024/1024) >= blockSizeLimit:
            write_dict_to_file(fileBaseName, fileIndex, block_dictionary)
            fileIndex += 1
            block_dictionary = {}


        tokenEntry_Token = getToken(tokenEntry)
        tokenEntry_DocID = getDocID(tokenEntry)

        if tokenEntry_Token in block_dictionary:

            if tokenEntry_DocID in block_dictionary[tokenEntry_Token]['docs'].keys():
                block_dictionary[tokenEntry_Token]['docs'][tokenEntry_DocID]['tf'] += 1

            else:
                block_dictionary[tokenEntry_Token]['df'] += 1
                block_dictionary[tokenEntry_Token]['docs'][tokenEntry_DocID] = {'tf': 1}

        else:
            block_dictionary[tokenEntry_Token] = {'df': 1, 'docs': {tokenEntry_DocID: {'tf': 1}}}

    # creates the last block
    write_dict_to_file(fileBaseName, fileIndex, block_dictionary)


# Writes the final inverted index on disk
def write_full_SPIMI_to_file(SPIMI_directory, full_SPIMI_dictionary):
    fileName = SPIMI_directory + 'SPIMI_dictionary.txt'
    # fileName = SPIMI_directory + 'Unfiltered_SPIMI/unfiltered_SPIMI_dictionary.txt'     # Uncomment to get unfiltered tokenStream
    dirName = os.path.dirname(fileName)

    if not os.path.exists(dirName):
        os.makedirs(dirName)

    with open(fileName, 'w') as blockFile:
        blockFile.write(json.dumps(full_SPIMI_dictionary, indent=2, sort_keys=True))

        print("SPIMI dictionary successfully saved to '" + fileName + "' file.")


# Merges all the blocks (mini inverted indexes) into one inverted index
def merge_SPIMI(SPIMI_directory, blockBaseName):
    fileList = [ f for f in os.listdir(SPIMI_directory) if f.startswith(blockBaseName) ]
    fileList = sorted(fileList)

    full_SPIMI_dictionary = {}

    for fname in fileList:
        blockFile_name = SPIMI_directory + fname

        with open(blockFile_name, 'r') as blockFile:
            file_content = blockFile.read()
            blockFile_dictionary = json.loads(file_content)

            for blockTerm, blockTerm_data in blockFile_dictionary.items():
                if blockTerm in full_SPIMI_dictionary:
                    full_SPIMI_dictionary[blockTerm]['df'] += blockTerm_data['df']
                    full_SPIMI_dictionary[blockTerm]['docs'].update(blockTerm_data['docs'])
                else:
                    full_SPIMI_dictionary[blockTerm] = {'df': blockTerm_data['df'], 'docs': blockTerm_data['docs']}

    write_full_SPIMI_to_file(SPIMI_directory, full_SPIMI_dictionary)




# Execution starts here
ts_file = 'Tokenization/tokenStream.txt'
# ts_file = 'Tokenization/unfiltered_tokenStream.txt'    # Uncomment to get unfiltered tokenStream

if os.path.isfile(ts_file):
    with open(ts_file, 'r') as tokenStream_file:
        file_content = tokenStream_file.read()
        tokenStream = json.loads(file_content)

        SPIMI_directory = 'SPIMI/'
        blockBaseName = 'spimi_block_'
        fileBaseName = SPIMI_directory + blockBaseName

        # Deletes all the previous files in the directory
        cleanDirectory(SPIMI_directory)

        SPIMI_Invert(tokenStream, fileBaseName)
        merge_SPIMI(SPIMI_directory, blockBaseName)

else:
    print("The tokenStream file was not found. Please run the 'Tokenizer.py' file first.")
