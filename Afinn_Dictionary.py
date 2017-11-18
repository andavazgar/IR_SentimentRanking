import os
import json

# Writes Afinn dictionary to disk
def write_dict_to_file(file_path, dictionary):
    dir_name = os.path.dirname(file_path)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    with open(file_path, 'w') as file:
        file.write(json.dumps(dictionary, indent=2, sort_keys=True))


afinn_file = 'AFINN/AFINN-111.txt'
afinn_dict_file = 'AFINN/afinnDictionary.txt'
afinn_dictionary = {}

with open(afinn_file) as f:
    afinn_content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
afinn_content = [x.strip() for x in afinn_content]

for term_with_sentiment in afinn_content:
    ts_arr = term_with_sentiment.split('\t')
    afinn_dictionary[ts_arr[0]] = ts_arr[1]

write_dict_to_file(afinn_dict_file, afinn_dictionary)
    
print("Afinn dictionary successfully saved to '" + afinn_dict_file + "' file.")

