import sys
import requests
import pageDiscovery
from urllib.parse import urlparse
from requests.exceptions import ConnectionError, MissingSchema, ReadTimeout

#DATA STRUCTURES
fuzzerSession = requests.Session()
queryDict = {}
vectors = []
sensitive = []
urls = []
commonWords = []

#GLOBAL SETTINGS
mode = ''
domain = ''
random = 0
slow = 500
pageExtensions = ['.html', '.aspx', '.jsp', '.jspx', '.php', '.asp', '.htm', '.do', '.rb', '.rhtml']


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
				pass
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
	global urls
	customAuthflag = False
	for x in range(3, sys.argv.__len__()):
		if '--common-words=' in sys.argv[x]:
			filePath = sys.argv[x][15:]
			wordFile = open(filePath)
			

			for line in wordFile:
				commonWords.append(line)
			wordFile.close()
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
main()