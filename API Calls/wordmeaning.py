'''
use from command line
API call to fetch the meaning of a word.

--requires (python)
requests
argparse

'''

import requests
import argparse

url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def Fetch_Word_Meaning(word):    
    repsonse = requests.get(url + word)
    data = repsonse.json()
    return data

def CommandLineCall():
    help_msg = "\n[-w] [--word] a word  :  Return meaning of the word"

    parser = argparse.ArgumentParser(description=help_msg)

    parser.add_argument("-w","--word",help="get word meaning")

    args = parser.parse_args()

    if args.word:
        return str(args.word).strip().lower().replace(" ",'')    
    return ""

def Main():
    word = CommandLineCall()
    if not word:
        print("Invalid Word.")
        return 

    # main
    meaning = Fetch_Word_Meaning(word)
    if not meaning:
        print("Word DNE")
        return 

    print(f'Meaning:\n {meaning[0]["meanings"][0]["definitions"][0]["definition"]}')



Main()
