'''
maproute.py

Called from command-line.

>>> python maproute.py -from "" -to ""

Returns a link to google map showing direction from and to place.
Note: This is not a display of "right" programming practices!

--requires (python)
argparse

'''

import argparse

def isValid(string):
    '''a string(here) is valid if doesn't contain special characters

    --returns
    if ok:
        True, string
    else:
        False, ""
    '''
    # ignore chars with a space
    # remove multiple spaces 
    # replace all spaces with +

    new_string = ""

    for i in string.lower().strip():
        if i.isalpha() or i.isdigit():
            new_string+=i
        elif i == " " and new_string[-1] != " ":
            new_string+=i

    if len(new_string) > 2:
        return True, new_string.replace(' ','+')
    else:
        return False, ""


def CommandLineCall():   

    parser = argparse.ArgumentParser(description="Get link to Google Map")

    parser.add_argument("-from","--f",help="from place")
    parser.add_argument("-to","--t",help="to place")

    args = parser.parse_args()
    isvalid_to, to = isValid(args.t)
    isvalid_fr, fr = isValid(args.f)

    if isvalid_to and isvalid_fr:
        url = "https://www.google.com/maps/dir/" + fr + "/" + to + "/"
        return url

    print('Invalid Input.')
    return None
    
    
url = CommandLineCall()
if url:
    print("Here's Your Direction Link")
    print('\t',url,end='\n')


