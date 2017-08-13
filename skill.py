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

	page = requests.get('http://secure.parking.ucf.edu/GarageCount/iframe.aspx')

	soup = BeautifulSoup(page.content, 'html.parser')

	newlist = list(soup.find_all('script', type="text/javascript"))
	i = 0
	garageNames = ['A', 'B', 'C', 'D', 'H', 'I', 'Libra']
	percentages = []
	message = ''
	for item in newlist:
		if('percent:' in item.get_text()):
			percent = re.findall('\d+', item.get_text())[1]
			if(garageNames[i] == "Libra"):
				print(garageNames[i] +" garage" +" is at " +percent+"% capacity")
				message = message + "<s>" + garageNames[i] +" garage" +" is at " +percent+" percent capacity </s>"
			else:
				print("Garage " + garageNames[i]+ " is at " + percent+"percent capacity")
				message = message + "<s>Garage " + garageNames[i]+ " is at " + percent+" percent capacity</s>"
			percentages.insert(i, percent)
			i+=1


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
