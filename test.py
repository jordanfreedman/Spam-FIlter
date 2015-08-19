import pandas as pd 
import re
import collections
import math
import os

# read email
email = open('/Users/jordanfreedman/Thinkful/Projects/Spam Filter/enron1/spam/0006.2003-12-18.GP.spam.txt', 'r').read()

# find individual words in email
def find_words(text):
	regex = r"[a-zA-Z0-9']+"
	all_words = re.findall(regex, text)
	return set(all_words)

# create dictionary with words as keys and number in email as value
def number_words(text):
	count = collections.defaultdict(int)
	words = list(find_words(text))
	for word in words:
		count[word] = text.count(word)
	return count

# calculate probability that spam email would contain word vector
def calc_probability(text, total_spam, total_ham):

	total = total_ham + total_spam
	prob_spam = float(total_spam)/total
	words_in_email = number_words(text)
	prob_email_spam = 0

	# remove 'Subject' which is present in all emails
	try: del words_in_email['Subject']
	except KeyError:
		pass
	
	# iterate through dictionary of words and number of inclusions
	for word, number in words_in_email.iteritems():

		# return number of spam emails with word
		no_spam_with_word = int(os.popen("grep -il " + word + " enron1/spam/*.txt | wc -l").read())

		# calculate probability that word vector found in spam 
		prob_in_spam = float(no_spam_with_word)/total_spam    #prob that word in spam
		wj_s = math.log(prob_in_spam/(1-prob_in_spam))
		w0_s = math.log(1-prob_in_spam)
		prob_s = (number * wj_s) + w0_s

		# return number of total emails with word
		no_ham_with_word = int(os.popen("grep -il " + word + " enron1/ham/*.txt | wc -l").read())
		total_with_word = no_ham_with_word + no_spam_with_word

		#calculate probability that word vector found in any email
		prob_in_total = float(total_with_word)/total     #prob that word in any email
		wj_t = math.log(prob_in_total/(1-prob_in_total))
		w0_t = math.log(1-prob_in_total)
		prob_t = (number * wj_t) + w0_t
		
		prob_word_spam = prob_s + math.log(prob_spam) - prob_t
		prob_email_spam += prob_word_spam
	# use naive bayers to calculate probability that word vector is spam
	return math.exp(prob_email_spam)

print calc_probability(email, 1500, 3672)










