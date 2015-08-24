import os
import re
import collections
import math 
import json

ham = '/Users/jordanfreedman/Thinkful/Projects/Spam_Filter/enron1/ham/'
spam = '/Users/jordanfreedman/Thinkful/Projects/Spam_Filter/enron1/spam/'
spam_email = '/Users/jordanfreedman/Thinkful/Projects/Spam_Filter/enron1/spam/0006.2003-12-18.GP.spam.txt'
database = 'spam_words_db.json'

def find_words(text):
	regex = r"[a-zA-Z0-9']+"
	all_words = re.findall(regex, text)
	return set(all_words)

def find_words_in_email(path):
	email = open(path, 'r')
	email_string = email.read()
	list_words_email = find_words(email_string)
	email.close()
	return set(list_words_email)

'''def find_words_in_folder(path):
	list_words_spam = []
	for file_name in os.listdir(path):
		email = open(path + file_name, 'r')
		email_string = email.read()
		list_words_email = find_words(email_string)
		new_words = list_words_email - set(list_words_spam)
		list_words_spam += list(new_words)
		email.close()
	return set(list_words_spam)'''

'''def number_in_folder(path):
	number = 0
	for file_name in os.listdir(path):
			number += 1
	return number'''

def create_vector(email_words, folder_words):
	vector = collections.defaultdict(int)
	for word in folder_words:
		if word in list(email_words):
			vector[word] = 1
		else:
			vector[word] = 0
	return vector

def calc_prob_email_spam(email, database):

	with open(database) as f:
	    spam_words = json.load(f)

	total_spam = spam_words['total_files']

	# words_in_folder = find_words_in_folder(folder)
	words_in_email = find_words_in_email(email)
	word_vector = create_vector(words_in_email, spam_words["words"]) # can i use dictionary?

	# remove 'Subject' which is present in all emails
	try: del spam_words["words"]['Subject']
	except KeyError: pass

	try: del spam_words["words"]["'"]
	except KeyError: pass

	total_prob_spam  = 0
	for word, binary in word_vector.iteritems():

		# return number of spam emails with word
		try: num_spam_with_word = spam_words['words'][word] 
		except KeyError: continue
		# calculate probability that word vector found in spam 
		prob_in_spam = float(num_spam_with_word)/total_spam   #prob that word in spam
		wj_s = math.log(prob_in_spam/(1-prob_in_spam))
		w0_s = math.log(1-prob_in_spam)
		prob_s = (binary * wj_s) + w0_s		
		total_prob_spam += prob_s    # add to sum
			
	return math.exp(total_prob_spam)

print calc_prob_email_spam(spam_email, database)














