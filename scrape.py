import requests
from bs4 import BeautifulSoup
import re

def main():
	print('Retrieving Garage Capacity info...')
	getGarageInfo()

def getGarageInfo():

	page = requests.get('http://secure.parking.ucf.edu/GarageCount/iframe.aspx')

	soup = BeautifulSoup(page.content, 'html.parser')

	newlist = list(soup.find_all('script', type="text/javascript"))
	i = 0
	garageNames = ['A', 'B', 'C', 'D', 'H', 'I', 'Libra']
	percentages = []
	for item in newlist:
		if('percent:' in item.get_text()):
			percent = re.findall('\d+', item.get_text())[1]
			if(garageNames[i] == "Libra"):
				print(garageNames[i] +" garage" +" is at " +percent+"% capacity")
			else:
				print("Garage " + garageNames[i]+ " is at " + percent+"% capacity")
			percentages.insert(i, percent)
			i+=1


	garageDict = dict(zip(garageNames,percentages))


def returnPercent(garageLetter, myDict):
	return myDict.get(garageLetter)



if __name__ == '__main__':
	main()
