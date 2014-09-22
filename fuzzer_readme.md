#Fuzzer Readme
___

Note: Fuzzer uses Python 3.4

Parameters:

1. Mode: Can either be Discover or Test
	* Discover crawls a given website and gathers a list of links and list of inputs throughout the site.
	* Test uses an external list of vectors in attempt to find vulnerabilities in the website and returns the results from the response. 
	* Note: The test mode is not included in the first release.
2. Domain: URL of the site you wish to Discover/Test on, should be in the format of http://www.websitename.domaintype where websitename is the name of the website and domaintype is the type of domain the site is using.
3. Custom Authentication (Optional): Enter --custom-auth= followed by a username and password separated by a comma to use for a website that requeires authentication. Note: This feature assumes the domain you entered is the login page for the website.
4. Common Words (Optional): Enter --common-words= followed by a file with a list of common words that is new-line delimited for the fuzzer to use to guess pages on the site. The default file included with the project is words.txt

Example:
	
1. Open Terminal or Command Prompt
2. Navigate to the directory of the project
3. Type in python (or your python path to 3.4) fuzzer.py discover http://www.yahoo.com --common-words=words.txt