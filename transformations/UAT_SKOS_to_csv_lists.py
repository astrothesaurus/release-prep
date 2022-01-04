#from collections import OrderedDict

import csv
import codecs
from datetime import datetime

lang_list = []

def getlangs(conceptlist):

    for iall in conceptlist:
        all_lits = lit2(iall)
        for t in all_lits:
            if t.language not in lang_list:
                lang_list.append(t.language)

def getinfo(conceptlist):

    for iall in conceptlist:
        print (iall)
        alternate = getaltterms(iall)
        altlist = []
        if alternate != None:
            for i in alternate:
                altlist.append(i)
        else:
            altlist = []
        lits = lit(iall)
        
        all_lits = lit2(iall)

        order = []
        for x in lang_list:
            for t in all_lits:
                if t.language == x:
                    order.append(t)

        if lits == None:
            #print("trying this")
            lits = getlabel(iall)

        ednote = getednotes(iall)
        #print (ednote)
        if ednote != None:
            for x in ednote:
                #print (x)

                edtitle = x["title"]
                edcomment = x["comment"]

                #print ("title: "+x["title"])
                #print ("comment: "+x["comment"])
            
        chnote = getchangenotes(iall)

                #print (ednote)
        if chnote != None:
            for x in chnote:
                #print (x)

                #print ("title: "+x["title"])
                #print ("comment: "+x["comment"])

                edtitle = x["title"]
                edcomment = x["comment"]



        scnote = getscopenotes(iall)
        ex = getexample(iall)
        define = getdefinition(iall)


        wr.writerow([lits]+altlist)
        wr2.writerow([lits])
        wr3.writerow([lits]+[iall])
        wr4.writerow([lits]+[ednote]+[chnote]+[scnote]+[ex]+[define])
        wr5.writerow([lits]+[scnote]+[ex]+[define])
        wr6.writerow([iall]+order)

resultFile6 = open("uat_all_languages"+timestamp+".csv",'w', encoding='utf-8-sig', newline='')
resultFile5 = open("uat_list_with_def_scope"+timestamp+".csv",'w', encoding='utf-8-sig', newline='')
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
wr5.writerow(["preferred term"]+["scope notes"]+["examples"]+["definition"])


getlangs(allconcepts)

print(lang_list)
wr6.writerow(["uri"]+lang_list)


getinfo(allconcepts)
#getinfo(alldepconcepts)

resultFile.close()
resultFile2.close()
resultFile3.close()
resultFile4.close()
resultFile5.close()
resultFile6.close()

print ("Finished. See uat_list"+timestamp+".csv and uat_list_with_alts"+timestamp+".csv")