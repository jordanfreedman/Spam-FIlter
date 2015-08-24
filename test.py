import os
import re
import collections
import math 
import json

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

'''def calc_prob_folder_has_email(email, database):

	with open(database) as f:
	    num_words_in_database = json.load(f)

	total_files = num_words_in_database['total_files']

	# words_in_folder = find_words_in_folder(folder)
	words_in_email = find_words_in_email(email)
	word_vector = create_vector(words_in_email, num_words_in_database["words"]) 

	# remove 'Subject' which is present in all emails
	try: del num_words_in_database["words"]['Subject']
	except KeyError: pass

	try: del num_words_in_database["words"]["'"]
	except KeyError: pass

	total_prob  = 0
	i = 0
	for word, binary in word_vector.iteritems():

		# return number of spam emails with word
		try: num_file_with_word = num_words_in_database['words'][word] 
		except KeyError: continue
		# calculate probability that word vector found in spam 
		prob_in_folder = float(num_file_with_word)/total_files   #prob that word in spam
		wj = math.log(prob_in_folder/(1-prob_in_folder))
		w0 = math.log(1-prob_in_folder)
		prob = (binary * wj) + w0	
		total_prob += prob    # add to sum
		i += 1
	print i
			
	return math.exp(total_prob)'''


def calc_prob_word_is_spam(email, spam_db, ham_db):

	with open(spam_db) as f:
	    num_words_in_spam = json.load(f)

	with open(ham_db) as f:
	    num_words_in_ham = json.load(f)
	
	all_words = num_words_in_spam.copy()
	all_words.update(num_words_in_ham)
	total_spam = num_words_in_spam['total_files']
	total_ham = num_words_in_ham['total_files']
	total = total_spam + total_ham
	prob_spam = float(total_spam) / total
	words_in_email = find_words_in_email(email)

	try: del all_words["words"]['Subject']
	except KeyError: pass
	try: del all_words["words"]["'"]
	except KeyError: pass

	number = 0
	total_spam_lg = 0
	total_s = 1
	for word in all_words["words"]:
		try: 
			num_spam_with_word = num_words_in_spam['words'][word] 
		except KeyError: 
			num_spam_with_word = 0
		try: 
			num_ham_with_word = num_words_in_ham['words'][word] 
		except KeyError: 
			num_ham_with_word = 0
		num_total_with_word = num_ham_with_word + num_spam_with_word
		prob_in_spam = float(num_spam_with_word)/num_total_with_word
		try:	wo_s = math.log(1 - prob_in_spam)
		except: wo_s = -25000
		total_spam_lg += wo_s
		if word in words_in_email:
			try: wj_s = math.log(prob_in_spam/(1-prob_in_spam))
			except: wj_s = -25000
			total_spam_lg += wj_s

		total_s += math.log(prob_spam)
		number += 1
	prob = total_spam_lg 
	prob /= number
	return math.exp(prob)


for file_name in os.listdir(ham):
	email = ham + file_name
	print calc_prob_word_is_spam(email, spam_database, ham_database)

