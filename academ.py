# -*- coding: utf-8 -*-
# This code will sort through a json file and look for swears assuming each line of the json has a element marked 'title'

import re
import json

#CONFIG STUFF

filename='../../../unpaywall_snapshot_2022-03-09T083001.jsonl' # data from here https://unpaywall.org/products/snapshot
swears="fuck piss shit cunt wank bastard penis cock vagina bugger bollock crap arse bitch fanny clunge gash prick minge stupid rubbish"


#HERE BE DRAGONS - the actual code

swears=swears.lower().split(" ")

def acro(title):
	title = title.replace("-", " ")
	title = title.replace("—", " ")
	title = re.sub(r"[^a-zA-Z ]+", "", title)
	title=title.lower()
	words = title.split()
	letters = [word[0] for word in words]
	acronym= "".join(letters)
	return(acronym)


def checkswear(title):
	ret=""
	for swear in swears:
		if swear in title:
			ret=ret+swear+" "

	if len(ret)==0:
		return False
	else:
		return ret.strip()

def reporton(title):
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



data = []
with open(filename) as f:
	for line in f:
		l= json.loads(line)
		title=l["title"]
		if title is not None:
			reporton (title)
