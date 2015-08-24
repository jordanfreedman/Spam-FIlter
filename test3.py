import os
import re
import collections
import math 
import json
from collections import Counter

ham = '/Users/jordanfreedman/Thinkful/Projects/Spam_Filter/enron2/ham/'
spam = '/Users/jordanfreedman/Thinkful/Projects/Spam_Filter/enron2/spam/'
spam_email = spam + '0006.2003-12-18.GP.spam.txt'
ham_email = ham + '0002.1999-12-13.farmer.ham.txt'
spam_database = 'spam_words_db.json'
ham_database = 'ham_words_db.json'


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

def number_in_folder(path):
	number = 0
	for file_name in os.listdir(path):
			number += 1
	return number

def create_vector(email_words, folder_words):
	vector = collections.defaultdict(int)
	for word in folder_words:
		if word in list(email_words):
			vector[word] = 1
		else:
			vector[word] = 0
	return vector

def calc_prob_word(word, database):

	total = database['total_files']
	lg_prob = 0
	try: num_with_word = database['words'][word] 
	except KeyError: num_with_word = 0
	prob = (float(num_with_word + 1)) / (total + 2)
	return prob
	
with open(spam_database) as f:
	    num_words_in_spam = json.load(f)

with open(ham_database) as f:
	    num_words_in_ham = json.load(f)

both_database = Counter(num_words_in_spam['words']) + Counter(num_words_in_ham['words'])
total = num_words_in_spam['total_files'] + num_words_in_ham['total_files']
num_words_in_all = {'total_files': total, 'words': both_database}

for file_name in os.listdir(spam):
	email = spam + file_name

	words_in_email = find_words_in_email(email)

	try: words_in_email.remove('Subject')
	except KeyError: pass

	try: words_in_email.remove("'")
	except KeyError: pass

	prob_spam = float(num_words_in_spam['total_files']) / num_words_in_all['total_files']
	lg_spam = 0
	lg_all = 0
	number = 0 
	for word in words_in_email: 
		lg_spam += math.log(calc_prob_word(word, num_words_in_spam))
		lg_all += math.log(calc_prob_word(word, num_words_in_all))
		number += 1
	try: prob = math.exp((lg_spam - lg_all) / number)
	except ZeroDivisionError: prob = 1.0 
	prob *= prob_spam

	if prob > 0.4:
		pass
		#print prob
	else: print prob
	
