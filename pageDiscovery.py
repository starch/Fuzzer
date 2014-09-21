from html.parser import HTMLParser
import requests

possibleWebsites = []
vistedWebsites = []
class HParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if tag == 'a' and len(attrs) > 0 and attrs[0] not in vistedWebsites:
			attrs = attrs[0]
			for element in attrs:
				if element.lower() == 'href':
					possibleWebsites.append(attrs)
					vistedWebsites.append(attrs)
					break

def generateAddress(domain, currentAddress, possibleAddress):
	if(possibleAddress[1][0] == "/"):
		return domain + possibleAddress[1]
	elif(possibleAddress[1][0:4].lower() == 'http'):
		if domain in possibleAddress[1]:
			return possibleAddress[1]
	else:
		index = 0;
		i = 0;
		while(i < len(currentAddress)):
			if currentAddress[i] == "/":
				index = i
				i = i + 1
		return currentAddress[0:index] + possibleAddress[1]
def testAddress(newaddress):
	try:
		r = requests.get(newaddress, timeout=10)
		return r.status_code
	except:    
			pass
	return -1;

def discoverWebpages(domain, url, ses):
	global possibleWebsites
	r = ses.get(url)
	parser = HParser()
	html = r.text
	parser.feed(html)
	validWebsites = []
	for websites in possibleWebsites:
		address = generateAddress(domain, url, websites)
		code = testAddress(address)
		if code == 200:
			validWebsites.append(address)
	possibleWebsites = []
	return validWebsites

def allValidWebPages(domain, url, ses):
	valid = discoverWebpages(domain, url, ses)
	result = valid
	while (len(valid) > 0):
		elements = discoverWebpages(domain,valid[0], ses)
		valid += elements
		valid = valid [1:]
		result += elements
	return result


