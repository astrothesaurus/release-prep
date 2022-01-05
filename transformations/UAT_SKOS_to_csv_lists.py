#from collections import OrderedDict

import csv
import codecs
from datetime import datetime

lang_list = []

def getlangs(conceptlist):

    for t in conceptlist:
        if getdepstatus(t) == None: # if concept is NOT deprecated
            all_lits = lit2(t)
            for t in all_lits:
                if t.language not in lang_list:
                    lang_list.append(t.language)

def getinfo(conceptlist):
    # rtotal = 0

    for t in conceptlist:
        if getdepstatus(t) == None: # if concept is NOT deprecated
            alternate = getaltterms(t)
            altlist = []
            if alternate != None:
                for i in alternate:
                    altlist.append(i)
            else:
                altlist = []
            lits = lit(t)
            
            all_lits = lit2(t)


            rts = getrelatedterms(t)
            if rts != None:
                for rt in rts:
                    wr6.writerow([lit(t)]+["is related to"]+[lit(rt)])
                    #rtotal+=1

            order = []
            for x in lang_list:
                for g in all_lits:
                    if g.language == x:
                        order.append(g)

            ednote = getednotes(t)
            edlist = []
            if ednote != None:
                for x in ednote:
                    edlist.append(str(x["title"])+": "+str(x["comment"]))    
            ednotes = (" | ").join(edlist)


            chnote = getchangenotes(t)
            chlist = []
            if chnote != None:
                for x in chnote:
                    chlist.append(str(x["title"])+": "+str(x["comment"]))            
            chnotes = (" | ").join(chlist)

            scnote = getscopenotes(t)

            # examples
            exa = getexample(t)
            if exa != None:
                exa = (", ").join(exa)

            define = getdefinition(t)

            wr.writerow([lits]+altlist)
            wr2.writerow([lits])
            wr3.writerow([lits]+[t])
            wr4.writerow([lits]+[ednotes]+[chnotes]+[scnote]+[exa]+[define])
            wr5.writerow([t]+order)

resultFile6 = open("relations"+timestamp+".csv",'w', encoding='utf-8', newline='')
resultFile5 = open("uat_all_languages"+timestamp+".csv",'w', encoding='utf-8-sig', newline='')
resultFile4 = open("uat_list_with_notes"+timestamp+".csv",'w', encoding='utf-8-sig', newline='')
resultFile3 = open("uat_list_with_uris"+timestamp+".csv",'w', encoding='utf-8-sig', newline='')
resultFile2 = open("uat_list"+timestamp+".csv",'w', encoding='utf-8-sig', newline='')
resultFile = open("uat_list_with_alts"+timestamp+".csv",'w', encoding='utf-8-sig', newline='')


wr = csv.writer(resultFile,quoting=csv.QUOTE_ALL)
wr2 = csv.writer(resultFile2,quoting=csv.QUOTE_ALL)
wr3 = csv.writer(resultFile3,quoting=csv.QUOTE_ALL)
wr4 = csv.writer(resultFile4,quoting=csv.QUOTE_ALL)
wr5 = csv.writer(resultFile5,quoting=csv.QUOTE_ALL)
wr6 = csv.writer(resultFile6,quoting=csv.QUOTE_ALL)

wr.writerow(["preferred term"]+["alternate terms"])
wr3.writerow(["preferred term"]+["uri"])
wr4.writerow(["preferred term"]+["editorial notes"]+["change notes"]+["scope notes"]+["examples"]+["definition"])
wr6.writerow(['.'])

getlangs(allconcepts)

print(lang_list)
wr5.writerow(["uri"]+lang_list)


getinfo(allconcepts)

resultFile.close()
resultFile2.close()
resultFile3.close()
resultFile4.close()
resultFile5.close()

print ("Finished. See uat_list"+timestamp+".csv and uat_list_with_alts"+timestamp+".csv")