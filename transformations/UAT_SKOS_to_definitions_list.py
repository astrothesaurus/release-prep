#from collections import OrderedDict

import csv
import codecs
from datetime import datetime

resultFile4 = open("uat_list_with_notes"+timestamp+".csv",'w', encoding='utf-8', newline='')

resultFile3 = open("uat_list_with_uris"+timestamp+".csv",'w', encoding='utf-8', newline='')
resultFile2 = open("uat_list"+timestamp+".csv",'w', encoding='utf-8', newline='')
resultFile = open("uat_list_with_alts"+timestamp+".csv",'w', encoding='utf-8', newline='')

wr = csv.writer(resultFile,quoting=csv.QUOTE_ALL)
wr2 = csv.writer(resultFile2,quoting=csv.QUOTE_ALL)
wr3 = csv.writer(resultFile3,quoting=csv.QUOTE_ALL)
wr4 = csv.writer(resultFile4,quoting=csv.QUOTE_ALL)

wr.writerow(["preferred term"]+["alternate terms"])
wr3.writerow(["preferred term"]+["uri"])
wr4.writerow(["preferred term"]+["editorial notes"]+["change notes"]+["scope notes"]+["examples"]+["definition"])

alltermlist = []
for iall in allconcepts:
    alternate = getaltterms(iall)
    altlist = []
    if alternate != None:
        for i in alternate:
            altlist.append(i)
    else:
        altlist = []
    lits = lit(iall)
    print (lits)
    if lits != None:

        ednote = getednotes(iall)
        chnote = getchangenotes(iall)
        scnote = getscopenotes(iall)
        ex = getexample(iall)
        define = getdefinition(iall)

        wr.writerow([lits]+altlist)
        wr2.writerow([lits])
        wr3.writerow([lits]+[iall])
        wr4.writerow([lits]+[ednote]+[chnote]+[scnote]+[ex]+[define.encode('utf-8')])

resultFile.close()
resultFile2.close()
resultFile3.close()
resultFile4.close()

print ("Finished. See uat_list"+timestamp+".csv and uat_list_with_alts"+timestamp+".csv")