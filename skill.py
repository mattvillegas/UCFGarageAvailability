import requests
from bs4 import BeautifulSoup
import re
from flask import Flask
from flask_ask import Ask, statement, question, session

# setting up Flask app
app = Flask(__name__)

ask = Ask(app, "/")

# launch intent immediately calls the Garage info function so that it is read off on launch
@ask.launch


def getGarageInfo():
	# downloads the HTML from the UCF Parking Garage page
	page = requests.get('http://secure.parking.ucf.edu/GarageCount/iframe.aspx')
	
	# turn the HTML into a BeautifulSoup object to parse
	soup = BeautifulSoup(page.content, 'html.parser')
	
	# separates all javascript scripts into a list to iterate through later
	newlist = list(soup.find_all('script', type="text/javascript"))
	
	i = 0 # need to fix this so I can just enumerate the for each loop
	garageNames = ['A', 'B', 'C', 'D', 'H', 'I', 'Libra']
	percentages = []
	message = ''
	
	# loop through each script in the list and find the percentages in the script
	for item in newlist:
		if('percent:' in item.get_text()):
			# some regex for getting the percentage as text
			percent = re.findall('\d+', item.get_text())[1] 
			# output formatting
			if(garageNames[i] == "Libra"):
				print(garageNames[i] +" garage" +" is at " +percent+"% capacity")
				# concatenates the print into a new string to return as a statement for Alexa
				message = message + "<s>" + garageNames[i] +" garage" +" is at " +percent+" percent capacity </s>"
			else:
				print("Garage " + garageNames[i]+ " is at " + percent+"percent capacity")
				message = message + "<s>Garage " + garageNames[i]+ " is at " + percent+" percent capacity</s>"
			percentages.insert(i, percent)
			i+=1 # still need to fix this using enumerate


	return statement("<speak>"+message+"</speak>")


# ask intents in case they want a repeat of the capacities
@ask.intent("Garage")
def Garage():
	print("Reached Garage Function")
	return getGarageInfo()
# for when the user asks for help
@ask.intent("AMAZON.HelpIntent")
def help():
	return statement("This skill tells you how full each of the garages are at UCF, just launching the skill should tell you the capacities")
	
if __name__ == '__main__':
	app.run(debug=True)
