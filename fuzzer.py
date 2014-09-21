import sys
import requests
import pageDiscovery
from urllib.parse import urlparse
from requests.exceptions import ConnectionError, MissingSchema, ReadTimeout

#DATA STRUCTURES
fuzzerSession = requests.Session()
queryStrings = []
links = []

#GLOBAL SETTINGS
mode = ''
domain = ''
vectors = []
sensitive = []
random = 0
slow = 500
pageExtensions = ['.html', '.aspx', '.jsp', '.jspx', '.php', '.asp', '.htm', '.do', '.rb', '.rhtml']
commonWords = []

def main():
	print('Fuzzer has started!')
	global domain
	global fuzzerSession

	if sys.argv.__len__() > 2 and sys.argv.__len__() <= 5:
		if sys.argv[1].lower() == 'discover':
			mode = 'discover'
		elif sys.argv[1].lower() == 'test':
			mode = 'test'

		domain = sys.argv[2].lower()

		try:
			r = requests.get(domain, timeout=10)

			if r.status_code == 200:
				print(domain + ' is a valid URL')
				print('')
				s = requests.Session()
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

	for x in range(3, sys.argv.__len__()):
		if '--common-words=' in sys.argv[x]:
			filePath = sys.argv[x][15:]
			wordFile = open(filePath)
			

			for line in wordFile:
				commonWords.append(line)
			wordFile.close()

		if '--custom-auth=' in sys.argv[x]:
			authString = sys.argv[x][14:]
			authString = authString.split(',')
			authUser = authString[0]
			authPass = authString[1]
			fuzzerSession.auth = (authUser, authPass)
			fuzzerSession.get(domain)

	guessPages()

	cookieFinder(fuzzerSession)

	for link in links:
		parseUrlForInput(link)

	for query in queryStrings:
		print('Printing Input ID\'s...')
		print('Input ID')
		print('=========')
		print(query)


def cookieFinder(sess):
	cookies = sess.cookies
	if cookies.__len__() < 1:
		print('No cookies')
	else:
		print('Printing cookies...')
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
		
	else:
		print("No query inputs")

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
main()