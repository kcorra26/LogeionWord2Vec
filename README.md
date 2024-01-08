# LogeionWord2Vec

The first step of the word2vec project is parsing xml files of various classical works and 
creating new files with additional attributes for each word. This is the first attempt with 
the xml file of Seneca's Agamemnon. For each word, the script accesses the LatinLexicon.sqlite 
database and adds the lemma and part of speech associated with the token. 

The edited files will eventually be fed to the word2vec model in order to update the Collocations
section of the Logeion, a free online dictionary that aggregates the resources of all the Latin 
and Greek dictionaries available through the Perseus Classical collection. 
