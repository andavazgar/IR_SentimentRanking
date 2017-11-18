import os
import platform
import subprocess

os_name = platform.system()

# Mac and Linux
if os_name in ['Darwin', 'Linux']:
    os.system("python3 Afinn_Dictionary.py")    # Generates Afinn_Dictionary
    os.system("python3 Tokenizer.py")   		# Generates tokenStream
    os.system("python3 SPIMI.py")       		# Generates inverted index
    os.system("python3 Query.py")       		# Asks for user queries


# Windows
elif os_name == 'Windows':
    subprocess.call("Afinn_Dictionary.py", shell = True)    # Generates Afinn_Dictionary
    subprocess.call("Tokenizer.py", shell = True)  		 	# Generates tokenStream
    subprocess.call("SPIMI.py", shell = True)      			# Generates inverted index
    subprocess.call("Query.py", shell = True)      		  	# Asks for user queries
