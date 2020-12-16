# coding: utf-8

import codecs

import csv

resultFile = open("relations"+timestamp+".csv",'w', encoding='utf-8', newline='')
wr = csv.writer(resultFile,quoting=csv.QUOTE_ALL)

wr.writerow(['.'])

rtotal = 0

for term in allconcepts:
    rts = getrelatedterms(term)
    if rts == None:
        pass
    else:
        for rt in rts:
            wr.writerow([lit(term)]+["is related to"]+[lit(rt)])
            rtotal+=1


resultFile.close()
print ('finished listing all related concept connections, total: '+str(rtotal))