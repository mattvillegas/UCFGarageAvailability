import requests
from bs4 import BeautifulSoup
import re
from flask import Flask
from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")


@ask.launch
def launchMsg():
	return statement("Hello. Please say the name of the garage")

# parses garage information into two lists
def getGarageInfo():
	# get HTML from the parking site
	page = requests.get('http://secure.parking.ucf.edu/GarageCount/iframe.aspx')

	# turn the site into a beautiful soup object
	soup = BeautifulSoup(page.content, 'html.parser')

	# create a list of all javascript scripts
	newlist = list(soup.find_all('script', type="text/javascript"))
	i = 0 # TODO: fix this so I can loop in a more pythonic way

	# create lists to store names of garages and their percentages
	garageNames = ['A', 'B', 'C', 'D', 'H', 'I', 'Libra']
	percentages = []

	# creates string that will be used for the alexa statement
	message = ''

	# loop through all of the scripts and insert values into the lists
	for item in newlist:

		# finds where the percentage is stored and uses regex to get the number from that string
		# the inserts into the list
		if('percent:' in item.get_text()):
			percent = re.findall('\d+', item.get_text())[1]
			percentages.insert(i, percent)
			i+=1 # see TODO above
	return garageNames, percentages

# creates a dictionary from the two lists 
def createGarageDict(listOne, listTwo):
	garageDict = dict(zip(listOne,listTwo))
	return garageDict

# called when the user asks for a specific garage
@ask.intent("Garage")
def Garage(GarageName):
	garageNames, percentages = getGarageInfo()
	garageDict = createGarageDict(garageNames,percentages)

	# capitalizes user input to make sure the dictionary is indexed properly
	GarageName = GarageName.capitalize()
	return statement("Garage {}".format(GarageName) + " is at {}".format(garageDict[GarageName]) + " percent capacity")

# called when the user aks for information for all garages
@ask.intent("AllGarages")
def sayAllGarages():
	garageNames, percentages = getGarageInfo()
	message = ''
	for i in range(0,7):
		message = message + "<s>Garage " + garageNames[i]+ " is at " + percentages[i] +" percent capacity</s>"

	return statement("<speak>" + message + "</speak>")

@ask.intent("AMAZON.HelpIntent")
def help():
	return statement("This skill tells you how full each of the garages are at UCF, just launching the skill should tell you the capacities")
	
if __name__ == '__main__':
	app.run(debug=True)
