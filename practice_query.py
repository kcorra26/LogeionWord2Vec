import sys
import os
#import xml.dom.minidom as md 
from xml.dom import minidom 
import io
import re
import shutil
import difflib
import unicodedata
import sqlite3
import gzip
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def main(): 
    #args = sys.argv[1:]
    filename = "SenAgLatPractice.xml"
    names = filename.split(".")
    nm = names[0] # find the original name of the file

    copyname = str(nm) + "_new.xml" #name of copied file
    cmd = "cp " + filename + " " + copyname
    
    copy = os.system(cmd)
    file = minidom.parse(copyname)

    dbh = sqlite3.connect("LatinLexicon.sqlite")
    dbc = dbh.cursor()

    bibliography = file.getElementsByTagName("w") #extracting only the word tags
    #for num, word in enumerate(bibliography):  for checking
    for word in bibliography:
        if word.hasAttribute("id"):
            token = word.getAttribute("id")

            dbc.execute("SELECT Lexicon.lemma,Lexicon.code FROM tokens,parses,Lexicon WHERE tokens.tokenid = ? and tokens.tokenid=parses.tokenid and parses.lex=Lexicon.lexid order by parses.prob desc;", (token,))
            result = dbc.fetchone()
            if result == None: # only two cases where this applies, we can do something different with it if needed
                dbc.execute("SELECT lemma,code from parses where tokenid=? order by prob desc;",(token,))
                result = dbc.fetchone()
                if result != None:
                    lemma = result[0] #just unknown but shows up funky
                    pos = "----------" 
                else:
                    print("not found in tokens or parses")
            else: 
                lemma = result[0]
                pos = result[1]

            word.setAttribute("lemma", lemma)
            word.setAttribute("pos", pos)

        #if num == 100:
            #break

    with open(copyname, "w") as f: #write changes into copied xml file
        f.write(file.toxml())
        f.close()

if __name__ == "__main__":
    main()
