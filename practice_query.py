#!/usr/local/bin/python3 *******FIGURE THIS OUT
import sys
import os
from xml.dom import minidom  # wondering if i should use lxml instead, but there
# should be a way to define the entities that are throwing errors with the og file. 
import io
import re
import shutil
import difflib
import unicodedata
import sqlite3
import gzip
#reload(sys)
#sys.setdefaultencoding('utf8')

# run with: python3 practice_query.py

def main(): 
    #args = sys.argv[1:]
    filename = input("Enter the file you would like to edit: ")

    # filename = "SenAgLat.xml"
    name = filename.split("/")
    names = name[1].split(".")
    nm = names[0] # find the original name of the file

    copyname = "newfiles/" + str(nm) + "_new.xml" #name of copied file
    cmd = "cp " + filename + " " + copyname
    
    copy = os.system(cmd)
    file = minidom.parse(copyname) 

    dbh = sqlite3.connect("dbses/LatinLexicon.sqlite")
    dbc = dbh.cursor()

    bibliography = file.getElementsByTagName("w") 
    print("length: ", len(bibliography))
    for word in bibliography:
        if (word.hasAttribute("id") and ((word.parentNode).tagName == "l")): 
        # this ONLY works for poetry -- need to find another way to check only valuable 
        # content for both prose and poetry (look into milestone tag)
            token = word.getAttribute("id")
            dbc.execute("SELECT Lexicon.lemma,Lexicon.code FROM tokens,parses,Lexicon WHERE tokens.tokenid = ? and tokens.tokenid=parses.tokenid and parses.lex=Lexicon.lexid order by parses.prob desc;", (token,))
            result = dbc.fetchone()
            if result == None: # only two cases where this applies, we can do something different with it if needed
                dbc.execute("SELECT lemma,code from parses where tokenid=? order by prob desc;",(token,))
                result = dbc.fetchone()
                if result != None: 
                    # either:
                    # unknown word, in which case: 
                    lemma = result[0]
                    # if unknown,
                    pos = "----------" 
                    # else, either a segment or legit lema 
                    pos = result[1]
                    # take lemma out of lemma, pos out of pos field 
                else:
                    print("one result not found in tokens or parses")
            else: 
                lemma = result[0]
                pos = result[1]

            word.setAttribute("lemma", lemma)
            word.setAttribute("pos", pos)

        #if num == 30:
            #break

    with open(copyname, "w") as f: #write changes into copied xml file
        f.write(file.toxml())
        f.close()

if __name__ == "__main__":
    main()
