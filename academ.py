# -*- coding: utf-8 -*-
# This code will sort through a json file and look for swears assuming each line of the json has a element marked 'title'

#%% Imports
import re
import json
import sys
import urllib 
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

#%% CONFIG STUFF

# NB: Changed to import function for word list. Defaults to original list above!

# data from here https://unpaywall.org/products/snapshot - this is 130GB when expanded, make sure you have the space
# filename='../../../unpaywall_snapshot_2022-03-09T083001.jsonl' 

# this list of swears is hardly definitive but it's quickly going to rack up CPU time with a bigger list
# swears="fuck piss shit cunt wank bastard penis cock vagina bugger bollock crap arse bitch fanny clunge gash prick minge stupid rubbish"
# NB: Changed to import function for word list. Defaults to original list above.

#HERE BE DRAGONS - the actual code

#swears=swears.lower().split(" ")


#%% FUNCTIONS

def importwords(location, column=""):
    words = []
    if location[-3:] == "txt":
        fileObj = open(location, "r")
        words = fileObj.read().splitlines()
        fileObj.close()
    elif location[-3:] == "csv":
        df = pd.read_csv(location)
        for index, row in df.iterrows():
            words.append(row[column])
    
    return words


def acro(title):
	# expects a string and returns an acronyn
	# removes non A-Z chars but treats hyphens as start of new word
	# makes everything lowercase in hope that we ultimately compare like with like
	 
	title = title.replace("-", " ")
	title = title.replace("—", " ")
	title = re.sub(r"[^a-zA-Z ]+", "", title)
	title=title.lower()
	words = title.split()
	letters = [word[0] for word in words]
	acronym= "".join(letters)
	return(acronym)


def checkswear(title, swears):
	# send it a string and it'll return swears listed in them
	# separated by a space, or return False if nothing is there
	# swears are defined as globals at the top baby
	
	ret=""
	for swear in swears:
		if swear in title:
			ret=ret+swear+" "

	if len(ret)==0:
		return False
	else:
		return ret.strip()
    

def reporton(title, wordlist):
	# send this a string and it'll send to standard out a report if it finds a swear in it
	# and say nothing if there's nothing to say
	 
    if len(str(title))>0:
        a=acro(title)
        cs=checkswear(a, wordlist)
        if cs is not False:
            out="'%s' in '%s' - %s" % (cs,a,title)
            if len(cs.split(" "))>1:
				# more than one swear - very special
                print ("double--> %s" % out)
            elif cs==a:
				# title exactly matches a swear
                print ("exact --> %s" % out)
            elif a.startswith(cs): 
				#title starts with a swear - as per the tweet
                print ("starts--> %s" % out)
            elif (abs(len(cs) - len(a)) <=1):
				#title is a swear plus a character (or minus one but that won't come up I think)
                print ("close --> %s" % out)
            else:
                print ("maybe --> %s" % out)
    else:
        print("Nothing there")
        return False
    

def loopfromfile(filename):
# this is (was) the main loop that's going to loop through the file, probably should sit in a MAIN thingie coz that's how you're meant to do shit init
# to make the output readable, you'll want to sort the output which I'm choosing to do in BBedit but you could do it with code if you want to
    data = []
    with open(filename) as f:
    	for line in f:
    		l= json.loads(line)
    		title=l["title"]
    		if title is not None:
    			reporton (title)
                
                
def loopfrompubmed(words, start, end, random=False, sample=100):
    titles = getpubmedtitles(start, end, random, sample)
    for t in titles:
        reporton(t, words)


def getpubmedtitles(start, end, random=False, sample=100):
    # Pass a start and end article index. If the random flag is set to True,
    # pick a sample of articles. Return as an array of strings.
    
    titles = []
    mainurl = "https://pubmed.ncbi.nlm.nih.gov/"
    
    if start <1: start = 0              # Limit results to the no. of articles in
    if end > 35500000: end = 35500000   # PubMed, else Bad Things will happen.
    
    def gettitle(id):
        # PubMed articles are hosted in date order using a simple ID. We just
        # need to iterate over these for the sample we're interested in.
        url = mainurl + str(id)
        try:
            # Some will have been withdrawn and a 404 error will be thrown.
            # This can be handled more elegantly but this'll do for now.
            html = urllib.request.urlopen(url)
            page = BeautifulSoup(html)
            return page.title.string
        except:
            return "Not Found"
    
    if not random:
        for i in range(start, end):
            print("Getting article " + str(id) + "/" + str(end-start) + ":")
            t = gettitle(i)
            titles.append(t)
            print("ID " + str(i) + " [" + t + "]")
            
    else:
        sampleindex = []
        a = 0
        while a < sample:
            pick = np.random.randint(start, end)
            if pick in sampleindex:
                pass
            else:
                sampleindex.append(pick)
                a += 1
        c = 1;
        for i in sampleindex:
            print("Getting article " + str(c) + "/" + str(len(sampleindex)) + ":")
            t = gettitle(i)
            titles.append(t)
            print("ID " + str(i) + " [" + t + "]")
            c += 1
                
    return titles



if __name__ == "__main__":
    # Test code here. 
    words = importwords("./Datasets/swears.txt")
    loopfrompubmed(words, 1, 5000, True, 10)
        
