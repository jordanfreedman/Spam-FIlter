# What is this?
It's a spam filter - your eternal guardian of unsolicited viagra sales. You've no doubt already got a much one, but this is generally how they work. Check out the files to take a look.

# What's in the files?
create_database.py - This collects all the words in the emails and counts how often they show up. It takes a while so it's stored in a JSON for whenever you need it.

spam.py - This is where the magic happens. This is where an email is classified as spam (or not) using Naive Bayes.

add_file.py - This is where the database is updated with a new email helping it learn.

ham_words_db.json - This is where all words and number of occurences for non-spam emails are stored.

spam_words_db.json - This is where all words and number of occurences for spam emails are stored.
