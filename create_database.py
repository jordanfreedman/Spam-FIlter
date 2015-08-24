# To save dictionaries with all words in email as well as number of emails where they are present

import os
import re
import collections
import math 
import json

ham = '/Users/jordanfreedman/Thinkful/Projects/Spam_Filter/enron1/ham/'
spam = '/Users/jordanfreedman/Thinkful/Projects/Spam_Filter/enron1/spam/'
spam_email = '/Users/jordanfreedman/Thinkful/Projects/Spam_Filter/enron1/spam/0006.2003-12-18.GP.spam.txt'


# return set of all words in string
def find_words(text):
	regex = r"[a-zA-Z0-9']+"
	all_words = re.findall(regex, text)
	return set(all_words)

# return set of all words in a folder of multiple files
def find_words_in_folder(path):
	list_words = []

	# loop through all files in folder
	for file_name in os.listdir(path):
		email = open(path + file_name, 'r') # open and read in file as string
		email_string = email.read()
		list_words_email = find_words(email_string)
		new_words = list_words_email - set(list_words) # remove repeated words
		list_words += list(new_words) # add new words to list of words
		email.close()
	return set(list_words)

# return number of files in folder
def number_in_folder(path):
	number = 0
	for file_name in os.listdir(path):
			number += 1
	return number

# return dictionary with keys as words in list and values as number of files found in
def number_file_with_word(words_list, folder):
	word_number = collections.defaultdict()
	number_files = number_in_folder(folder) 
	word_number["total_files"] = number_files # save total number of files for future use when finding probabilities
	word_number["words"] = collections.defaultdict(int) # create nested dictionary to save words
	# loop through each word in list
	for index,word in enumerate(words_list):
		num_word = 0
		regex = r"(\b" + word + r"\b)" # regular expression will search for whole word
		# loop through files in folder
		for file_name in os.listdir(folder): 
			path = folder + file_name
			fh = open(path, 'r')
			word_present = re.findall(regex, fh.read()) # check whether word is present using regex
			number = len(word_present)
			if number > 0:
				num_word += 1 # if word found more than once, add 1 to num_words
			fh.close()
		word_number["words"][word] = num_word # save number of files found in as value to word key 
		print index
	return word_number

# find all words in ham folder
a = find_words_in_folder(ham)

# return dictionary of all words and their respective number of files present
spam_words = number_file_with_word(a, ham)

print spam_words

# save dictionary as JSON for future use
with open('ham_words_db.json', 'w') as f:
	json.dump(spam_words, f)

