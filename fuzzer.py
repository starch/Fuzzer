import sys
import urllib2
import requests

def main():
	print('Fuzzer has started!')
	mode = ''
	domain = ''
	vectors = []
	sensitive = []
	random = 0
	slow = 500
	print(sys.argv.__len__())
	if sys.argv.__len__() >= 1 and sys.argv.__len__() <= 5:
		if sys.argv[1].lower() == 'discover':
			mode = 'discover'
		elif sys.argv[1].lower() == 'test':
			mode = 'test'

		domain = sys.argv[2].lower()
		r = requests.get(domain)

		if r.status_code == 200:
			print(domain + ' is a valid URL')

			if mode == 'discover':
				#Call discover function here
				discoverHelper()
			elif mode == 'test':
				#Call test function here
				pass
		else:
			print(domain + ' is not a valid URL')
			pass

def discoverHelper():

	for x in range(3, sys.argv.__len__()):
		if '--common-words=' in sys.argv[x]:
			filePath = sys.argv[x][15:]
			wordFile = open(filePath)
			commonWords = []

			for line in wordFile:
				commonWords.append(line)
			wordFile.close()
		if '--custom-auth=' in sys.argv[x]:
			authString = sys.argv[x][14:]
			authString.split(',')
			authUser = authString[0]
			authPass = authString[1]

main()