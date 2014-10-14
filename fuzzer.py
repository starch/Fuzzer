import sys
import requests
import pageDiscovery
from urllib.parse import urlparse
from requests.exceptions import ConnectionError, MissingSchema, ReadTimeout

#DATA STRUCTURES
fuzzerSession = requests.Session()
queryStrings = []
links = []
slowLinks = []
responseCodeLinks = []
SensitiveDataLinks = []

#GLOBAL SETTINGS
mode = ''
domain = ''
vectors = []
sensitive = []
urls = []
random = 0
slow = 500
pageExtensions = ['.html', '.aspx', '.jsp', '.jspx', '.php', '.asp', '.htm', '.do', '.rb', '.rhtml']
commonWords = []
sensitiveWords = []

def main():
	print('Fuzzer has started!')
	global domain
	global fuzzerSession
	global mode

	if sys.argv.__len__() > 2 and sys.argv.__len__() <= 5:
		if sys.argv[1].lower() == 'discover':
			mode = 'discover'
		elif sys.argv[1].lower() == 'test':
			mode = 'test'

		domain = sys.argv[2].lower()

		try:
			r = fuzzerSession.get(domain, timeout=10)

			if r.status_code == 200:
				print(domain + ' is a valid URL')
				print('')
				fuzzerSession.get(domain)
			if mode == 'discover':
				#Call discover function here
				discoverHelper()

			elif mode == 'test':
				#Call test function here
				discoverHelper()

		except ConnectionError as e:    
			print(domain + ' is not responding')
		except MissingSchema as m:
			print(domain + ' is not a valid URL')
		except ReadTimeout as t:
			print('Request to ' + domain + ' timed out')

	else:
		print('Please enter a fuzzer mode followed by a domain')

def discoverHelper():
	global domain
	global fuzzerSession
	global commonWords
	global sensitiveWords
	global urls
	customAuthflag = False
	for x in range(3, sys.argv.__len__()):
		if '--common-words=' in sys.argv[x]:
			filePath = sys.argv[x][15:]
			wordFile = open(filePath)
			

			for line in wordFile:
				commonWords.append(line)
			wordFile.close()
		if '--sensitive-words=' in sys.argv[x]:
			filePath = sys.argv[x][18:]
			wordFile = open(filePath)
			

			for line in wordFile:
				sensitiveWords.append(line)
			wordFile.close()
		if '--custom-auth=' in sys.argv[x]:
			customAuthflag = True
			authString = sys.argv[x][14:]
			if(authString.lower() == "dvwa"):
				payload = {"username":"admin", "password":"password","Login":"Login"}
				fuzzerSession.post("http://127.0.0.1/dvwa/login.php", data=payload)
				temp = (fuzzerSession.get("http://127.0.0.1/dvwa/index.php"))
				urls = pageDiscovery.allValidWebPages("http://127.0.0.1/dvwa/", "http://127.0.0.1/dvwa/index.php", fuzzerSession)

	guessPages()

	cookieFinder(fuzzerSession)

	if urls.__len__() < 1:
		print('No URL\'s found')
	else:
		print('URL')
		print('===')
		for url in urls:
			print(url)
	print('')

	inputs = pageDiscovery.getInput()

	if inputs.__len__() < 1:
		print('No inputs found')
	else:
		print('Input ID')
		print('=======')
		for i in inputs:
			print(i)
	print('')

	for link in links:
		parseUrlForInput(link)

	if queryStrings.__len__() < 1:
		print('No query string inputs')
	else:
		print('Input ID')
		print('=======')
		for query in queryStrings:
			print(query)
	if not customAuthflag:
		urls = pageDiscovery.allValidWebPages(domain, domain, fuzzerSession)

def cookieFinder(sess):
	cookies = sess.cookies
	if cookies.__len__() < 1:
		print('No cookies')
	else:
		print('Cookie Name \t Cookie Value')
		print('=============================')
		for c in cookies:
			print(c.name + '\t\t\t\t' + c.value)
	print('')

def parseUrlForInput(url):
	result = urlparse(url)
	#should be in the form: query=something
	queryString = result.query
	if queryString != '':
		queryAry = queryString.split('&')
		for q in queryAry:
			qStr = q.partition('=')
			#should return the "query" component
			queryStrings.append(qStr[0])

def guessPages():
	global links
	global commonWords

	for word in commonWords:
		if domain[-1] == '/':

			for ext in pageExtensions:

				urlGuess = domain + word + ext

				try:
					r = requests.get(urlGuess, timeout=3)

					if r.status_code == 200:
						links.append(urlGuess)
				except ConnectionError as e:    
					pass
				except MissingSchema as m:
					pass
				except ReadTimeout as t:
					pass
		else:

			for ext in pageExtensions:

				urlGuess = domain + '/' + word + ext
				
				try:
					
					r = requests.get(urlGuess, timeout=3)

					if r.status_code == 200:
						links.append(urlGuess)
				except ConnectionError as e:    
					pass
				except MissingSchema as m:
					pass
				except ReadTimeout as t:
					pass

def responseChecker(testUrl):
	global slowLinks
	global responseCodeLinks
	global slow

	seconds = slow / 1000

	try:
		r = requests.get(testUrl, timeout=seconds)

		if r.status_code != 200:
				responseCodeLinks.append(testUrl)
	except ConnectionError as e:    
		pass
	except MissingSchema as m:
		pass
	except ReadTimeout as t:
		slowLinks.append(testUrl)

def sensitiveDataChecker(testUrl):
	global sensitiveWords
	global fuzzerSession
	global SensitiveDataLinks

	r = fuzzerSession.get(testUrl)
	html = r.text

	for word in sensitiveWords:
		if word in html:
			SensitiveDataLinks.append(testUrl)


main()