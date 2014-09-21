import requests
import urllib.request
from html.parser import HTMLParser


possibleWebsites = []
class LinkParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if len(attrs) > 0 and attrs[0] not in possibleWebsites:
			attrs = attrs[0]
			for element in attrs:
				if element.lower() == 'href':
					possibleWebsites.append(attrs)
					break
		

def getHtml(url):
	req = urllib.request.Request(url)
	response = urllib.request.urlopen(req)
	the_page = response.read()
	return the_page.decode()

def testAddress(domain, currentAddress, possibleAddress):
	i = 0
	validAddress = []
	if(possibleWebsites[i][1][0] == "/"):
		index = 0;
		i = 0;
		while(i > len(currentAddress)):
			if currentAddress[i] == "/":
				index = i
				i = i + 1


parser = LinkParser()
html = getHtml('http://www.w3schools.com/tags/tag_figcaption.asp')
parser.feed(html)
"""for array in possibleWebsites:
	for touple in array:
		for element in touple:
			if element == 'href':
				print("true")"""
#print(possibleWebsites)
for websites in possibleWebsites:
	print(websites)