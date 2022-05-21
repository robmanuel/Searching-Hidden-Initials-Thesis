# -*- coding: utf-8 -*-
# This code will sort through a json file and look for swears assuming each line of the json has a element marked 'title'

import re
import json

#CONFIG STUFF

# data from here https://unpaywall.org/products/snapshot - this is 25GB compressed (each line can be decompressed individually)
filename='../../../unpaywall_snapshot_2022-03-09T083001.jsonl' 

# this list of swears is hardly definitive but it's quickly going to rack up CPU time with a bigger list
swears="fuck piss shit cunt wank bastard penis cock vagina bugger bollock crap arse bitch fanny clunge gash prick minge stupid rubbish"


#HERE BE DRAGONS - the actual code

swears=swears.lower().split(" ")

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


def checkswear(title):
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

def reporton(title):
	# send this a string and it'll send to standard out a report if it finds a swear in it
	# and say nothing if there's nothing to say
	 
	if len(str(title))>0:
		a=acro(title)
		cs=checkswear(a)
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
		return False

# this is the main loop that's going to loop through the file, probably should sit in a MAIN thingie coz that's how you're meant to do shit init
# to make the output readable, you'll want to sort the output which I'm choosing to do in BBedit but you could do it with code if you want to

import gzip
with gzip.open(filename,'rt') as f:
	for line in f:
		l= json.loads(line)
		title=l["title"]
		if title is not None:
			reporton (title)
