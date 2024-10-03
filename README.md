# LogeionWord2Vec

This project uses the word2vec model to draw collocated relationships between words in Greek and Latin texts.
It serves as a prototype for an incoming feature for Logeion, a free classical search engine site and database that 
aggregates the resources of all the Latin and Greek dictionaries available through the Perseus Classical collection. 

## Preprocessing: 
The script parses the xml files containing the classical texts and creates a new file for each one. For each word, 
the script queries the LatinLexicon.sqlite database and adds the lemma and part of speech associated with the token 
as attributes of the word tag in the new file. This preprocessing significantly improves the efficiency of the model 
below. 

## The Model:
The edited files are then processed to make up the corpus for the Word2Vec model, in which the words are stored
by sentence, reduced to their lemmas, and given numerical values in relation to other words. 

Deployment to Logeion is in progress.
