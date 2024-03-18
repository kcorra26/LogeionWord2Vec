import os
import sys
import xml.etree.ElementTree as ET
import io
import re
#import sqlite3

import gensim
import gensim.models

from gensim.models import Word2Vec

#NOTE: run this file with $ python3 making_model.py
    
def parse_with_et():
    filename = "SenAgLatPractice_new.xml"
    
    tree = ET.parse(filename)
    root = tree.getroot()

    sentences = []
    current_sentence = []

    for line in root.findall('.//l'):

        # Iterate over all 'w' tags within the current 'l' tag
        for word in line.findall('w'):
            # Extract the lemma of each word
            if word.get('lemma'):  # NOTE: could also check its tag and exclude if pos = preposition or something
                current_sentence.append(word.get('lemma'))
            
            # Check for punctuation in the tail text of the word
            if word.tail and ('.' in word.tail or '?' in word.tail): # NOTE: if Greek, need to add semicolon
                # We found a period in the tail text
                sentences.append(current_sentence)
                current_sentence = []
    for sentence in sentences: 
        print(sentence)
    return sentences
    #for sentence in sentences: 
        #print(sentence) NOTE: Going to need to make sure that these sentences are right, but pretty sure they are


def main(): 
    stnces = parse_with_et() #making a list of sentences from xml texts
    data_dir = "corpus"
    os.chdir(data_dir)

    model = Word2Vec(sentences=stnces, vector_size=100, window=5, min_count=1, workers=4) #research these later
    model.save("word2vec.model")

    # for testing: 
    w1 = "decem" 
    print(model.wv.most_similar (positive=w1))


if __name__ == "__main__":
    main()
