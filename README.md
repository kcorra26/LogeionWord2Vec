# LogeionWord2Vec

The practice_query.py script updates the attributes in the word tags of xml files containing 
various classical works. This is the first attempt with the xml file of Seneca's Agamemnon. 
The script accesses the LatinLexicon.sqlite database and adds the lemma and part of speech 
for each word. 

The edited files will eventually be fed to the word2vec model in order to update the Collocations
section of the Logeion, a free online dictionary that aggregates the resources of all the Latin 
and Greek dictionaries available through the Perseus Classical collection. 
