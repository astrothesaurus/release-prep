# coding: utf-8
## This scripts compares two versions of the UAT and generates
## information such as new concepts, deprecated concepts
## new related links, new alt labels, new pref labels, etc etc.
## Data is useful in creating the release notes

import os
import csv
import json
import codecs
import shutil
import rdflib
import unicodedata
#import pandas as pd
from datetime import datetime

timestamp = datetime.now().strftime("%Y_%m%d_%H%M")

print ("Reading the SKOS file...this may take a few seconds.")
##### RDF File Location #####
##### assign this variable to location of UAT SKOS-RDF file exported from VocBench ##### 

##export RDF/XML Concepts
uat_new = "uat_new.rdf" # filename for the new version

#get previous version RDF from GitHub
uat_prev = "UAT_4.0.1.rdf" # filename for the previous version

##### Shared Functions and Variables #####
##### do NOT edit this section #####

#reads SKOS-RDF file into a RDFlib graph for use in these scripts
g = rdflib.Graph()
result = g.parse(uat_new)#.encode('utf8'))

f = rdflib.Graph()
result = f.parse(uat_prev)#.encode('utf8'))

#defines certain properties within the SKOS-RDF file
prefLabel = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#prefLabel')
broader = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#broader')
Concept = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#Concept')
vocstatus = rdflib.term.URIRef('http://art.uniroma2.it/ontologies/vocbench#hasStatus')
altLabel = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#altLabel')
TopConcept = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#topConceptOf')
ednotes = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#editorialNote')
changenotes = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#changeNote')
scopenotes = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#scopeNote')
example = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#example')
related = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#related')
definition = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#definition')
comment = rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#comment')
title = rdflib.term.URIRef('http://purl.org/dc/terms/title')
label = rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#label')

#a list of all concepts
allnewconcepts = [gm for gm in g.subjects(rdflib.RDF.type, Concept)]

allprevconcepts = [fm for fm in f.subjects(rdflib.RDF.type, Concept)]

def lit(term):
    d = rdflib.term.URIRef(term)
    for prefterm in g.objects(subject=d, predicate=prefLabel):
        return prefterm

def deplit(term):
    d = rdflib.term.URIRef(term)
    for prefterm in f.objects(subject=d, predicate=prefLabel):
        return prefterm


#a function to get a list of all alt terms for a term
def getaltterms(term,version):
    terminal = rdflib.term.URIRef(term)
    alternateterms = {}
    try:
        for ats in version.objects(subject=terminal, predicate=altLabel):
            try:
                alternateterms[terminal].append(ats)
            except KeyError:
                alternateterms[terminal] = [ats]
        return alternateterms[terminal]
    except KeyError:
        pass 

#a function to get a list of all related terms for a term
def getrelatedterms(term,version):
    terminal = rdflib.term.URIRef(term)
    relatedterms = {}
    try:
        for rts in version.objects(subject=terminal, predicate=related):
            try:
                relatedterms[terminal].append(rts)
            except KeyError:
                relatedterms[terminal] = [rts]
        return relatedterms[terminal]
    except KeyError:
        pass  

#a function to get a list of all broader terms for a term
def getbroaderterms(term,version):
    terminal = rdflib.term.URIRef(term)
    broaderterms = {}
    try:
        for bts in version.objects(subject=terminal, predicate=broader):
            try:
                broaderterms[terminal].append(bts)
            except KeyError:
                broaderterms[terminal] = [bts]
        return broaderterms[terminal]
    except KeyError:
        pass


#a function to return scope notes for a term
def getscopenotes(term,sf):
    d = rdflib.term.URIRef(term)
    for scnoteterm in sf.objects(subject=d, predicate=scopenotes):
        return scnoteterm

#a function to return example notes for a term
def getexample(term,sf):
    d = rdflib.term.URIRef(term)
    exlist = []
    for termex in sf.objects(subject=d, predicate=example):
        exlist.append(termex)
    return exlist

#a function to return the status of a term    
def getdefinition(term,sf):
    d=rdflib.term.URIRef(term)
    for deftest in sf.objects(subject=d, predicate=definition):
        return deftest


fileout = open('changes_'+timestamp+'.csv','w', encoding='utf-8', newline='')

csv_out = csv.writer(fileout, lineterminator='\n', delimiter=',')
wr = csv.writer(fileout,quoting=csv.QUOTE_ALL)#
#UnicodeWriter(fileout,lineterminator='\n', delimiter=',', dialect='excel',quoting=csv.QUOTE_ALL)

##prints all new concepts, new alts, removed alts

for newcon in allnewconcepts:
    if newcon in allprevconcepts:
        newalts = getaltterms(newcon, g)
        oldalts = getaltterms(newcon, f)

        copynewalts = getaltterms(newcon, g)
        copyoldalts = getaltterms(newcon, f)

        if oldalts == None or newalts == None :
            pass

        else:
            for x in newalts:
                if x in oldalts:
                    copynewalts.remove(x)

            for y in oldalts:
                if y in newalts:
                    copyoldalts.remove(y)

        if copyoldalts != None and copyoldalts != []:
            aoldalts = (", ").join(copyoldalts)
            wr.writerow((["Removed Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+[aoldalts]+[" |"]))

        if copynewalts != None and copynewalts != []:
            anewalts = (", ").join(copynewalts)
            wr.writerow((["New Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+[anewalts]+[" |"]))

    #         depaltlist = []
    #         for y in oldalts:
    #             if y in newalts:
    #                 pass
    #             else:
    #                 depaltlist.append(y)
    #         if depaltlist != []:
    #             for z in depaltlist:
    #                 if z == lit(newcon):
    #                     pass
    #                 else:
    #                     wr.writerow((["Removed Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+depaltlist+[" |"]))
    else:
        litterm = lit(newcon)        
        morealts = getaltterms(newcon, g)           

        wr.writerow(("New concept",newcon[30:],"| ",newcon," | ",litterm," |"))
        if morealts != None:
            amorealts = (", ").join(morealts)
            wr.writerow((["New Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+[amorealts]+[" |"]))

##finds all deprecated concepts
for oldcon in allprevconcepts:
    if oldcon in allnewconcepts:
        oldlit = deplit(oldcon)
        newlit = lit(oldcon)
        if oldlit != newlit:
            wr.writerow(("Updated PrefLabel",oldcon[30:],"| ",oldcon," | ",oldlit," | ",newlit," |"))
    else:
        litterm = deplit(oldcon)
        wr.writerow(("Deprecated concept",oldcon[30:],"| ",oldcon," | ",litterm," |"))


#finds all new related links
relatedlist = []

for oldcon in allprevconcepts:
    litterm = lit(oldcon)
    rterms = getrelatedterms(oldcon,f)
    if rterms != None:
        for x in rterms:
            littermx = lit(x)
            relatedlist.append([oldcon,x])

newrelatedlist = []
for newcon in allnewconcepts:
    litterm = lit(newcon)
    rterms = getrelatedterms(newcon,g)
    if rterms != None:
        for x in rterms:
            littermx = lit(x)
            newrelatedlist.append([newcon,x])
            if [newcon,x] in relatedlist:
                pass
            else:
                wr.writerow(("Related",newcon[30:],"| ",newcon," | ",litterm," | ",x," | ",littermx," |"))



#finds all new defintions, scope notes, examples
deflist = []
scopelist = []
examplelist = []
for oldcon in allprevconcepts:
    olddef = getdefinition(oldcon,f)
    oldscope = getscopenotes(oldcon,f)
    oldex = getexample(oldcon,f)

    if olddef != None:
        deflist.append([oldcon,olddef])

    if oldscope != None:
        scopelist.append([oldcon,oldscope])

    if oldex != None:
        examplelist.append([oldcon,oldex])

for newcon in allnewconcepts:
    newdef = getdefinition(newcon,g)
    newscope = getscopenotes(newcon,g)
    newex = getexample(newcon,g)
    litterm = lit(newcon)

    if newdef != None:
        if [newcon,newdef] not in deflist:
            wr.writerow(("Definition",newcon[30:],"| ",newcon," | ",litterm," | ",newdef," |"))

    if newscope != None:
        if [newcon,newscope] in scopelist:
            pass
        else:
            wr.writerow(("Scope Note",newcon[30:],"| ",newcon," | ",litterm," | ",newscope," |"))

    if newex != []:
        if [newcon,newex] in examplelist:
            pass
        else:
            nex = ", ".join(newex)
            wr.writerow(("Example",newcon[30:],"| ",newcon," | ",litterm," | ",nex," |"))


#gets removed related links
for a in relatedlist:
    if a in newrelatedlist:
        pass
    else:
        wr.writerow(("Removed Related",a[0][30:],"| ",a[0]," | ",deplit(a[0])," | ",a[1]," | ",deplit(a[1])," |"))

fileout.close()

print ("finished!")