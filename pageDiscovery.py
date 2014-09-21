import requests
import urllib.request
from html.parser import HTMLParser
import requests


possibleWebsites = []
test = []
class LinkParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if tag == 'a' and len(attrs) > 0 and attrs[0] not in possibleWebsites:
			attrs = attrs[0]
			test.append(attrs)
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
	if(possibleAddress[1][0] == "/"):
		newaddress = domain + possibleAddress[1]
	elif(possibleAddress[1][0:4].lower() == 'http'):
		newaddress = possibleAddress[1]
	else:
		index = 0;
		i = 0;
		while(i < len(currentAddress)):
			if currentAddress[i] == "/":
				index = i
				i = i + 1
				print("s")
		newaddress = currentAddress[0:index] + possibleAddress[1]
	try:
		r = requests.get(newaddress, timeout=10)
		return r.status_code
	except ConnectionError as e:    
			print(domain + ' is not responding')
	except MissingSchema as m:
			print(domain + ' is not a valid URL')
	return -1;

address = "http://www.greenberg.com"
parser = LinkParser()
html = getHtml(address)
parser.feed(html)
print((possibleWebsites))
for websites in possibleWebsites:
	print(websites)
	print(testAddress(address, address, websites))
print("Stop")