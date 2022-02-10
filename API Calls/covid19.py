'''
covid19.py
API call to get India/state data of COVID-19 Cases

--requires (python)
request
json
argparse

'''

import requests
import json
import argparse

class API:

    def __init__(self, _url):
        self.url = _url
        self.data = {}
        self.isAPIActive = False
        try:
            self._response = requests.get(self.url)
            self.data = self._response.json()
            self.isAPIActive = True
        except:
            print("Failed to Connect to API - Please Check the URL!")

        if self.isAPIActive and not self.data['success']:            
            self.isAPIActive = False

    @property
    def Data(self):
        if self.isAPIActive:
            return self.data
        else:
            return {}


def PolishString(string, makelower= False):
    '''Removes extra whitespaces from string'''    
    string = string.strip()

    if makelower:
        return string.lower()
    else:
        return string

def isaMatch(word,string):
    '''checks how much a word matches in a string    
    eg.
    isaMatch("uttrpradhesh", "Uttar Pradesh")-> 60%
    
    --return
    percentage: float
    '''
    # a very minimal probability of string matching algorithm
    # just count all macthing character 
    # return 100% if abbr provided for two word string
    # eg. UP -> Uttar Pradesh => 100% match
    # otherwise direct matching

    word = PolishString(word,True)
    string = PolishString(string,True)

    len_word = len(word)
    len_string = len(string)

    # if word len 2 and string word count 2
    if len_word == 2 and string.count(' ') == 1:
        _string = string.split(' ')        
        if (word[0] == _string[0][0]) and (word[1] == _string[1][0]):
            return 100

    # else direct sorting match    
    _stringList = {c:string.count(c) for c in set(string)}
    _wordList = sorted(list(word))

    _count_chars = 0

    # pop from _stringList and count
    for i in _wordList:
        if i in _stringList and _stringList[i] > 0:
            _stringList[i] -= 1
            _count_chars += 1

    if string[0] == word[0]:
        if string[1] == word[1]:
            return _count_chars * 100 / len_word
        
        
    return _count_chars * 100 / len_string

def GetStateData(state, api,getMatch = False):
    '''Returns the Data of the State else India if ""

    --args
    state: str = name of the state
    [getMatch: bool] : return plausible matches (if available)

    --return    
    (True, dataDictionay) ; if state found

    <if getMatch = False>
    (False, {}, "") : if state name not found
    
    <if getMatch = True>
    (False, matchData, bestMatch: str) : if state name not found
    '''
    if (not api.isAPIActive):
        return (False, {}, "")

    
    if (state == ""):        
        _regionData = api.Data['data']['summary']
        return True, _regionData, []
    _india_match_prob = isaMatch(state, "india")

    # get the most probable match
    _best_match = ""
    _best_match_prob = 0
    _best_match_data = {}

    for _regionData in api.data['data']['regional']:
        if (_regionData["loc"].lower() == state.lower()) or (isaMatch(state,_regionData["loc"]) == 100):
            return True,_regionData, []
        
        if (getMatch):
            _this_prob = isaMatch(state,_regionData["loc"])
            if _this_prob > _best_match_prob:
                _best_match = _regionData["loc"]                
                _best_match_data = _regionData
                _best_match_prob = _this_prob
                #print(_best_match,_best_match_prob)

    if _india_match_prob > _best_match_prob:
        _regionData = api.Data['data']['summary']
        return (False, _regionData, "India")

    return (False, _best_match_data, _best_match)

def FormatKeyString(string):
    '''Splits and capitalise each Main Word'''    
    _output = string[0].upper()

    for s in string[1:]:
        if s.isupper():
            _output += " "
        _output += s

    return _output

def PrintData(data):
        #_data = stateCovidData[1]
        for key,value in data.items():
            print (f"{FormatKeyString(key):<25} : {value:<10}")

def CommandLineCall():
    help_msg = "\n[-s] [--state] stateName  :  Return data about the state, if emtpy => country\n"

    parser = argparse.ArgumentParser(description=help_msg)

    parser.add_argument("-s","--state",help="show state data")

    args = parser.parse_args()

    if args.state:
        return str(args.state)

    return ""

def main(cmdline_access = False):

    # make api call    
    apiURL = "https://api.rootnet.in/covid19-in/stats/latest"
    covidAPI = API(apiURL)

    if (not covidAPI.isAPIActive):
        print("API is Not Active : Can't Make the Request.")
        return 
    
    # get user input
    if cmdline_access:
        stateName = CommandLineCall()
    else:
        stateName = input('State Name: ', )

    stateName = PolishString(stateName)

    # get region's data
    stateCovidData = GetStateData(stateName, covidAPI,getMatch = True)

    # if found
    if (stateCovidData[0]):
        if stateName == "":
            PrintData({"loc":"India"})        
        PrintData(stateCovidData[1])
    
    else: 
        # if not found but Match Exists
        if stateCovidData[2]:
            print(f"Did you mean: {stateCovidData[2]} ? " ,end='')
            user_input = input('(Yes/No) >')
            user_input = PolishString(user_input)

            if user_input in 'yes':
                print()
                PrintData(stateCovidData[1])
            
        else:
            # if not found
            print("Invalid State Name. Program End....!")
            return

    print("\nVisit Again. Program End.....!")
    print()

#----------------------------

# Assume all Access from CommandLine
# otherwise make changes here....!

main(True)

