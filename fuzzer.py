import sys
import requests
import random
import pageDiscovery
from urllib.parse import urlparse
from requests.exceptions import ConnectionError, MissingSchema, ReadTimeout

#DATA STRUCTURES
fuzzerSession = requests.Session()
queryDict = {}
sensitive = []
urls = []
commonWords = []
slowLinks = []
responseCodeLinks = []
sensitiveDataLinks = []
unsanitizedLinks = []


#GLOBAL SETTINGS
mode = ''
domain = ''
randomFuzz = 0
slow = 500
pageExtensions = ['.html', '.aspx', '.jsp', '.jspx', '.php', '.asp', '.htm', '.do', '.rb', '.rhtml']
sensitiveWords = []
vector = []

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
	global randomFuzz
	global slow
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
		if '--vectors=' in sys.argv[x]:
			filePath = sys.argv[x][10:]
			vectorFile = open(filePath)
		

			for line in vectorFile:
				vector.append(line)
			vectorFile.close()
		if '--random=' in sys.argv[x]:
			randomSetting = sys.argv[x][9:]

			if randomSetting.lower() == 'true':
				randomFuzz = 1
			elif randomSetting.lower() == 'false':
				randomFuzz = 0;
		if '--slow=' in sys.argv[x]:
			slowSetting = sys.argv[x][7:]

			if slowSetting.isdigit():
				slow = slowSetting
		if '--custom-auth=' in sys.argv[x]:
			customAuthflag = True
			authString = sys.argv[x][14:]
			if(authString.lower() == "dvwa"):
				payload = {"username":"admin", "password":"password","Login":"Login"}
				fuzzerSession.post("http://127.0.0.1/dvwa/login.php", data=payload, timeout=3)
				urls = pageDiscovery.allValidWebPages("http://127.0.0.1/dvwa/", "http://127.0.0.1/dvwa/index.php", fuzzerSession)
			if(authString.lower() == "bodgeit"):
				reg = {"username":"admin@admin.com", "password":"password1","password":"password2","Login":"Login"}
				fuzzerSession.post("http://127.0.0.1:8080/bodgeit/register.jsp", data=reg)
				login = {"username":"admin@admin.com", "password":"password","Login":"Login"}
				fuzzerSession.post("http://127.0.0.1:8080/bodgeit/login.jsp", data=login)
				urls = pageDiscovery.allValidWebPages("http://127.0.0.1:8080/", "http://127.0.0.1:8080/bodgeit/home.jsp", fuzzerSession)
			if not customAuthflag:
				urls = pageDiscovery.allValidWebPages(domain, domain, fuzzerSession)
	guessPages()
	cookieFinder(fuzzerSession)
	queryUrl = []
	i = 0
	while(i < len(urls)):
		if("?" in urls[i]):
			queryUrl.append(urls[i])
			substring = urls[i][0 : urls[i].index("?")]
			if(substring in urls):
				urls.remove(urls[i])
			else:
				urls[i] = substring
				i+=1
		else:
			i+=1

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

	for url in urls + queryUrl:
		parseUrlForInput(url)

	if queryDict.__len__() < 1:
		print('No query string inputs')
	else:
		print('Query strings')
		print('=======')
		for key, value in queryDict.items():
			print('Query strings for ' + key)
			print('=======')
			for i in value:
				print(i)
			print('')



def testHelper():
	global randomFuzz
	global vector
	global fuzzerSession
	global slowLinks
	global responseCodeLinks
	global slow
	global queryDict

	seconds = slow / 1000

	if randomFuzz == 1:
		#insert randomization here
		randomUrlInt = random.randrange(0, urls.__len__()+1)
		randomUrl = urls[randomUrlInt]

		randomInputInt = random.randrange(0, len(pageDiscovery.getinputDict(randomUrl))+1)
		randomInput = pageDiscovery.getinputDict(randomUrl)[randomInputInt]

		for vectorData in vector:
			payload = {randomInput: vectorData}
			#send POST Ruquest here
			try:
				r = fuzzerSession.post(randomUrl, data=payload, timeout=seconds)
					
				if r.status_code != 200:
					responseCodeLinks.append(randomUrl)
				else:
					html = r.text
					sensitiveDataChecker(randomUrl, html)
			except ConnectionError as e:    
				pass
			except MissingSchema as m:
				pass
			except ReadTimeout as t:
				slowLinks.append(randomUrl)

	elif randomFuzz == 0:
		for url in urls:
			for inputs in pageDiscovery.getInputDict(url):
				for vectorData in vector:
					payload = {inputs: vectorData}
					#send POST Request here
				try:
					r = fuzzerSession.post(url, data=payload, timeout=seconds)
					
					if r.status_code != 200:
						responseCodeLinks.append(url)
					else:
						html = r.text
						sensitiveDataChecker(url, html)
				except ConnectionError as e:    
					pass
				except MissingSchema as m:
					pass
				except ReadTimeout as t:
					slowLinks.append(url)	
			for query in queryDict[url]:
				for vectorData in vector:
					replaceQueryStrings(url, vectorData)


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
	global queryDict
	result = urlparse(url)
	#should be in the form: query=something
	queryString = result.query
	key = url
	if queryString != '':
		if key not in queryDict:
			queryDict[key] = []
		queryAry = queryString.split('&')
		for q in queryAry:
			qStr = q.partition('=')
			#should return the "query" component
			queryDict[key].append(qStr[0])

def guessPages():
	global commonWords

	for word in commonWords:
		if domain[-1] == '/':

			for ext in pageExtensions:

				urlGuess = domain + word + ext

				try:
					r = requests.get(urlGuess, timeout=3)

					if r.status_code == 200:
						urls.append(urlGuess)
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
						urls.append(urlGuess)
				except ConnectionError as e:    
					pass
				except MissingSchema as m:
					pass
				except ReadTimeout as t:
					pass

def sensitiveDataChecker(testUrl, html):
	global sensitiveWords
	global fuzzerSession
	global SensitiveDataLinks

	for word in sensitiveWords:
		if word in html:
			sensitiveDataLinks.append(testUrl)
def checkSanatization(url, html, vector):
	global unsanitizedLinks
	before = ["<",">","&",'"']
	after = ["&lt","&gt","&amp;","&quot;"]
	if before in vector:
		if vector in html:
			unsanitizedLinks += url

def replaceQueryStrings(url, data):
	result = urlparse(url)
	#should be in the form: query=something
	queryString = result.query
	if queryString != '':
		queryAry = queryString.split('&')
		count = 0
		for q in queryAry:
			old = q
			qStr = q.partition('=')
			new = qStr[0] + "=" + data[count]
			url.replace(old, new)
			count += 1
		return url
	else:
		return ""

def printTest():
	global urls = []
	global slowLinks = []
	global responseCodeLinks = []
	global sensitiveDataLinks = []
	global unsanitizedLinks = []

	if urls in (slowLinks + responseCodeLinks + sensitiveDataLinks + unsanitizedLinks):
		print(urls)
		if urls in slowLinks:
			print("This url timed out when fuzzed")
		if urls in responseCodeLinks:
			print("The response code was not 200 when fuzzed")
		if urls in sensitiveDataLinks:
			print("Senesitive data may have been linked")
		if urls in unsanitizedLinks:
			print("The input was not sanitized")
		print("\n")

main()