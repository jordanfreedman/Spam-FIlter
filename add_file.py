# To add new emails to saved dictionary of words and their respective number of files present in 

import json
import collections
import os

spam = '/Users/jordanfreedman/Thinkful/Projects/Spam_Filter/enron1/spam/'
file_name = '4201.2005-04-05.GP.spam.txt'

# load dictionary
with open('spam_words_db.json') as f:
    spam_words = json.load(f)

def find_words(text):
	regex = r"[a-zA-Z'][a-zA-Z0-9]+"
	all_words = re.findall(regex, text)
	return set(all_words)

def find_words_in_email(path):
	email = open(path, 'r')
	email_string = email.read()
	list_words_email = find_words(email_string)
	email.close()
	return set(list_words_email)	


if file_name not in os.listdir(spam): # check if file already in folder
	path = spam + file_name
	try: # if file exists, add new words and counts of add to existing counts.
		words = find_words_in_email(path)
		for word in words:
			spam_words["words"][word] += 1
		spam_words["total_files"] += 1 # add 1 to number of files
		print "new file added"
	except IOError:  # if file doesn't exist, let user know
		print "this file doesn't exist"
	
else: # if file already in folder, let user know
	print "already in folder"


