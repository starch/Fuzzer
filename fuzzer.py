import sys
import urllib2
import requests
from requests.exceptions import ConnectionError, MissingSchema
from urllib.parse import urlparse

#DATA STRUCTURES
queryStrings = []

#GLOBAL SETTINGS
mode = ''
domain = ''
vectors = []
sensitive = []
random = 0
slow = 500
pageExtensions = ['.html', '.aspx', '.jsp', '.php', '.asp']

def main():
	print('Fuzzer has started!')

	if sys.argv.__len__() > 2 and sys.argv.__len__() <= 5:
		if sys.argv[1].lower() == 'discover':
			mode = 'discover'
		elif sys.argv[1].lower() == 'test':
			mode = 'test'

		domain = sys.argv[2].lower()

		try:
			r = requests.get(domain, timeout=3)

			if r.status_code == 200:
				print(domain + ' is a valid URL')

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

	else:
		print('Please enter a fuzzer mode followed by a domain')

def discoverHelper():

	for x in range(3, sys.argv.__len__()):
		if '--common-words=' in sys.argv[x]:
			filePath = sys.argv[x][15:]
			wordFile = open(filePath)
			commonWords = []

			for line in wordFile:
				commonWords.append(line)
			wordFile.close()

			for word in commonWords:
				if domain[-1] == '/':

					for ext in pageExtensions:

						urlGuess = domain + word + ext

						try:
							r = requests.get(urlGuess, timeout=3)

							if r.status_code == 200:
								#Add to link array
								pass
						except ConnectionError as e:    
							pass
				   		except MissingSchema as m:
				   			pass
			   	else:

			   		for ext in pageExtensions:

				   		urlGuess = domain + '/' + word + ext
				   		
				   		try:
							
							r = requests.get(urlGuess, timeout=3)

							if r.status_code == 200:
								#Add to link array
								pass
						except ConnectionError as e:    
							pass
				   		except MissingSchema as m:
				   			pass

		if '--custom-auth=' in sys.argv[x]:
			authString = sys.argv[x][14:]
			authString = authString.split(',')
			authUser = authString[0]
			authPass = authString[1]
			login = requests.get(domain, auth=(authUser, authPass))


def cookieFinder(url):
	req = requests.get(url)
	cookies = req.cookies
	if cookies.__len__ < 1:
		print('No cookies')
	else:
		for c in cookies:
			print(c + '\n')

def parseUrlForInput(url):
	result = urlparse(url)
	#should be in the form: query=something
	queryString = result.query
	qStr = queryString.partition('=')
	#should return the "query" component
	queryStrings.append(qStr[0])

main()