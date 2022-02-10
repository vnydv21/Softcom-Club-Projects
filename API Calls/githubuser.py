'''
githubuser.py

Returns a few data about the github user.
(A few line are inefficient cause repeated API calls are being)

WIP: function required to return Most Used progamming language.

--required
requests
json

'''

import requests
import json

def FetchData(url):
    '''
    --return
    if found: data
    else: None
    '''
    try:
        repsonse = requests.get(url)
        data = repsonse.json()

    except:
        print("Connection Failed")
        return None

    # custom code ------
    if ('message' in data):
        if data['message'].lower().strip() == "not found":
            print("Not Found")
        else:
            print(data['message'].lower().strip())
        return None

    return data


def GetValidField(data):
    ''' Valid Field Required
    avatarUrl : avatar_url
    userHandle : login    
    fullName : name
    bio : bio
    gitHubLink : html_url
    location ["" => Private] : location
    joined: "created_at"

    followers: followers
    latestEvent() = {event, type, date}

    top3_languages = (totalFound:3, [lang1 : %share,,,, other: %share])
    '''

    # Print_Label : API_keys
    
    keys = ['login','name','bio','avatar_url','html_url','location',
            'followers', 'created_at','public_repos']

    for i in keys:
        print (f"{i:<20} : {data[i]}")

    # print repo data
    repourl = data['repos_url']

    # fetch each url and sum all langauges code
    data = FetchData(repourl)    
    languages = {}

    for repo in data:
        language_data = FetchData(repo['languages_url'])

        for lang in language_data:
            if lang in languages:
                languages[lang] += language_data[lang]
            else:
                languages[lang] = language_data[lang]

    print(json.dumps(languages, indent=4))



# assumes no space exists in username
URL = "https://api.github.com/users/"

data = FetchData(URL+input('UserName:').strip().lower().replace(' ',''))

if data:
    print(f"LoginId: {data['id']}")
    GetValidField(data)
    

