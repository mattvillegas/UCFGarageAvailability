import requests
from bs4 import BeautifulSoup
import re
from flask import Flask
from flask_ask import Ask, statement, question

# boilerplate to set up Flask
app = Flask(__name__)

ask = Ask(app, "/")

# launch message
@ask.launch
def launchMsg():
    return question("Welcome to UCF Garage information. For help, say help")

# parses garage information into two lists
def getGarageInfo():
   
    # get HTML from the parking site
    page = requests.get(
        'http://secure.parking.ucf.edu/GarageCount/iframe.aspx')

    # turn the site into a beautiful soup object
    soup = BeautifulSoup(page.content, 'html.parser')

    # create a list of all javascript scripts
    newlist = list(soup.find_all('script', type="text/javascript"))
    i = 0  # TODO: fix this so I can loop in a more pythonic way

    # create lists to store names of garages and their percentages
    garageNames = ['A', 'B', 'C', 'D', 'H', 'I', 'Libra']
    percentages = []

    # loop through all of the scripts and insert values into the lists
    for item in newlist:

        # finds where the percentage is stored
        # then uses regex to get the percentage from text
        # then inserts into the list
        if('percent:' in item.get_text()):
            percent = re.findall('\d+', item.get_text())[1]
            percentages.insert(i, percent)
            i += 1  # see TODO above
    return garageNames, percentages

# creates a dictionary from two lists
def createGarageDict(listOne, listTwo):
    garageDict = dict(zip(listOne, listTwo))
    return garageDict

# called when the user asks for a specific garage
@ask.intent("Garage")
def Garage(GarageName):
    garageNames, percentages = getGarageInfo()
    garageDict = createGarageDict(garageNames, percentages)

    # capitalizes user input to make sure the dictionary is indexed properly
    GarageName = GarageName.capitalize()
    return statement("Garage {}".format(GarageName) +
                     " is at {}".format(garageDict[GarageName]) +
                     " percent capacity")

# called when the user asks for information for all garages
@ask.intent("AllGarages")
def sayAllGarages():
    garageNames, percentages = getGarageInfo()
    message = ''
    for i in range(0, 7):
        message = message + "<s>Garage " + \
            garageNames[i] + " is at " + \
            percentages[i] + " percent capacity</s>"

    return statement("<speak>" + message + "</speak>")

# help message
@ask.intent("AMAZON.HelpIntent")
def help():
    return statement(
        "This skill tells you how full each of the garages are at UCF,"
        "and can tell you which garage is the emptiest. "
        "To hear the capacities of individual garages,"
        "you can ask how full is garage A. "
        "To hear the capacities of all of the garages, you can say all. "
        "To hear which garage is the emptiest, ask what is the emptiest garage"
    )

# called when the user wants to know the emptiest garage
@ask.intent("EmptiestGarage")
def findEmptiest():
    garageNames, percentages = getGarageInfo()
    minIndex = 0
    minPercentage = 100
    for i in range(0, 7):
        if(int(percentages[i]) < minPercentage):
            minPercentage = int(percentages[i])
            minIndex = i

    return statement("Garage {}".format(garageNames[minIndex]) +
                     " is the emptiest at {}".format(percentages[minIndex]) +
                     " percent capacity")


if __name__ == '__main__':
    app.run(debug=True)
