import requests
from bs4 import BeautifulSoup
import re

def main():
	print('Retrieving Garage Capacity info...')
	getGarageInfo()

def getGarageInfo():
	#Get the HTML from the UCF parking page
	page = requests.get('http://secure.parking.ucf.edu/GarageCount/iframe.aspx')
	
	#Parse it with beautiful soup
	soup = BeautifulSoup(page.content, 'html.parser')
	
	#create a list of all javascript scripts in the html file
	newlist = list(soup.find_all('script', type="text/javascript"))
	i = 0 #need to update so that I can use for i in range which isn't working
	
	garageNames = ['A', 'B', 'C', 'D', 'H', 'I', 'Libra']
	percentages = []
	
	#loop through all the scripts and pull the garage percentages from inside the script
	for item in newlist:
		if('percent:' in item.get_text()):
			percent = re.findall('\d+', item.get_text())[1] #some regex for getting the actual digit for the percentage
			#text formatting based on the garage name
			if(garageNames[i] == "Libra"):
				print(garageNames[i] +" garage" +" is at " +percent+"% capacity")
			else:
				print("Garage " + garageNames[i]+ " is at " + percent+"% capacity")
			percentages.insert(i, percent)
			i+=1 #ugh very much unpythonic

def returnPercent(garageLetter, myDict):
	return myDict.get(garageLetter)



if __name__ == '__main__':
	main()
