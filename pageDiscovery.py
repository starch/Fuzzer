from html.parser import HTMLParser
import requests

possibleWebsites = []
vistedWebsites = []
inputList = []
class HParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		global vistedWebsites
		global inputList
		if tag == 'a' and len(attrs) > 0 and attrs[0] not in vistedWebsites:
			attrs = attrs[0]
			for element in attrs:
				if element != None and element.lower() == 'href':
					possibleWebsites.append(attrs)
					vistedWebsites.append(attrs)
					break
		elif tag == 'input' and len(attrs) > 0:
			for name, value in attrs:
				if name == 'id':
					inputList.append(value)
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
		print(currentAddress[0:index] + "/" + possibleAddress[1])
		return currentAddress[0:index] + "/" + possibleAddress[1]
def testAddress(newaddress):
	try:
		r = requests.get(newaddress, timeout=3)
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
		print(websites)
		if ("logout" in websites[1].lower() or "log-out" in websites[1].lower() or "log_out" in websites[1].lower()) != True:
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

def getInput():
	global inputList
	return inputList