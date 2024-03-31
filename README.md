# LogeionWord2Vec

This project uses the word2vec model to add a word vector/collocation feature for Logeion, a free online 
learning site and app that aggregates the resources of all the Latin and Greek dictionaries available 
through the Perseus Classical collection. 

## Preprocessing: 
The script parses the xml files containing the classical texts and creates a new file for each one. For each word, 
the script queries the LatinLexicon.sqlite database and adds the lemma and part of speech associated with the token 
as attributes of the word tag in the new file.

## The Model:
The edited files are then processed to make up the corpus for the Word2Vec model, in which the words are stored
by sentence and reduced to their lemmas. 
