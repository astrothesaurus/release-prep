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
import cStringIO
import unicodedata
#import pandas as pd
from datetime import datetime

timestamp = datetime.now().strftime("%Y_%m%d_%H%M")

#UnicodeWriter from http://docs.python.org/2/library/csv.html#examples
class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

#/end UnicodeWriter

print "Reading the SKOS file...this may take a few seconds."

##### RDF File Location #####
##### assign this variable to location of UAT SKOS-RDF file exported from VocBench ##### 

##export RDF/XML Concepts
uat_new = "UAT3.1.rdf" # filename for the new version

#get previous version RDF from GitHub
uat_prev = "UAT3.0.rdf" # filename for the previous version

##### Shared Functions and Variables #####
##### do NOT edit this section #####

#reads SKOS-RDF file into a RDFlib graph for use in these scripts
g = rdflib.Graph()
result = g.parse((uat_new).encode('utf8'))

f = rdflib.Graph()
result = f.parse((uat_prev).encode('utf8'))

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
termdef = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#definition')
example = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#example')
related = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#related')


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
def getscopenotes(term):
    d = rdflib.term.URIRef(term)
    for scnoteterm in g.objects(subject=d, predicate=scopenotes):
        return scnoteterm

#a function to return example notes for a term
def getexample(term):
    d = rdflib.term.URIRef(term)
    for termex in g.objects(subject=d, predicate=example):
        return termex

#a function to return the status of a term    
def getdefinition(term):
    d=rdflib.term.URIRef(term)
    for deftest in g.objects(subject=d, predicate=termdef):
        return deftest


fileout = codecs.open('changes_'+timestamp+'.csv', 'wb')

csv_out = csv.writer(fileout, lineterminator='\n', delimiter=',')
wr = UnicodeWriter(fileout,lineterminator='\n', delimiter=',', dialect='excel',quoting=csv.QUOTE_ALL)

##prints all new concepts, new alts, removed alts

for newcon in allnewconcepts:
    if newcon in allprevconcepts:

        newalts = getaltterms(newcon, g)
        oldalts = getaltterms(newcon, f)

        if oldalts == None and newalts == None :
            pass
        elif oldalts == None and newalts != None:

            anewalts = (", ").join(newalts)

            wr.writerow((["New Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+[anewalts.encode("utf-8")]+[" |"]))
        elif oldalts != None and newalts == None:
            wr.writerow((["Removed Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+[aoldalts.encode("utf-8")]+[" |"]))
        elif oldalts != None and newalts != None:

            aoldalts = (", ").join(oldalts)

            altlist = []
            for x in newalts:
                if x in oldalts:
                    pass
                else:
                    altlist.append(x)

            aaltlist = (", ").join(altlist)
            if altlist != []:
                wr.writerow((["New Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+[aaltlist.encode("utf-8")]+[" |"]))

            depaltlist = []
            for y in oldalts:
                if y in newalts:
                    pass
                else:
                    depaltlist.append(y)
            if depaltlist != []:
                for z in depaltlist:
                    if z == lit(newcon):
                        pass
                    else:
                        wr.writerow((["Removed Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+depaltlist+[" |"]))
    else:
        litterm = lit(newcon)        
        morealts = getaltterms(newcon, g)           

        wr.writerow(("New concept",newcon[30:],"| ",newcon," | ",litterm.encode("utf-8")," |"))
        if morealts != None:
            amorealts = (", ").join(morealts)
            wr.writerow((["New Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+[amorealts]+[" |"]))
        else:
            pass


##finds all deprecated concepts
for oldcon in allprevconcepts:
    if oldcon in allnewconcepts:
        oldlit = deplit(oldcon)
        newlit = lit(oldcon)
        if oldlit != newlit:
            #print oldlit
            #print newlit
            wr.writerow(("Updated PrefLabel",oldcon[30:],"| ",oldcon.encode("utf-8")," | ",oldlit.encode("utf-8")," | ",newlit.encode("utf-8")," |"))
        else:
            pass

    else:
        litterm = deplit(oldcon)
        wr.writerow(("Deprecated concept",oldcon[30:],"| ",oldcon," | ",litterm.encode("utf-8")," |"))


#finds all new related links
relatedlist = []

for oldcon in allprevconcepts:
    litterm = lit(oldcon)
    rterms = getrelatedterms(oldcon,f)
    if rterms == None:

        pass
    else:
        for x in rterms:
            littermx = lit(x)
            relatedlist.append([oldcon.encode("utf-8"),x.encode("utf-8")])
            #csv_out.writerow(("old related",oldcon.encode("utf-8"),litterm.encode("utf-8"),x.encode("utf-8"),littermx.encode("utf-8")))


newrelatedlist = []
for newcon in allnewconcepts:
    litterm = lit(newcon)
    #print "concept: "+ newcon
    rterms = getrelatedterms(newcon,g)
    if rterms == None:

        pass
    else:
        for x in rterms:
            littermx = lit(x)
            newrelatedlist.append([newcon.encode("utf-8"),x.encode("utf-8")])
            if [newcon.encode("utf-8"),x.encode("utf-8")] in relatedlist:
                pass
            else:
                csv_out.writerow(("Related",newcon[30:],"| ",newcon.encode("utf-8")," |",litterm.encode("utf-8")," | ",x.encode("utf-8")," | ",littermx.encode("utf-8")," |"))



#finds all new defintions, scope notes, examples
deflist = []
scopelist = []
examplelist = []
for oldcon in allprevconcepts:
    olddef = getdefinition(oldcon)
    oldscope = getscopenotes(oldcon)
    oldex = getexample(oldcon)

    if olddef == None:
        pass
    else:
        deflist.append([oldcon.encode("utf-8"),olddef.encode("utf-8")])

    if oldscope == None:
        pass
    else:
        scopelist.append([oldcon.encode("utf-8"),oldscope.encode("utf-8")])

    if oldex == None:
        pass
    else:
        examplelist.append([oldcon.encode("utf-8"),oldex.encode("utf-8")])


for newcon in allnewconcepts:
    newdef = getdefinition(newcon)
    newscope = getscopenotes(newcon)
    newex = getexample(newcon)
    litterm = lit(newcon)

    if newdef == None:
        pass
    else:
        if [newcon.encode("utf-8"),newdef.encode("utf-8")] in deflist:
            pass
        else:
            csv_out.writerow(("Definition",newcon[30:],"| ",newcon.encode("utf-8")," |",litterm.encode("utf-8")," |",newdef.encode("utf-8")," |"))

    if newscope == None:
        pass
    else:
        if [newcon.encode("utf-8"),newscope.encode("utf-8")] in scopelist:
            pass
        else:
            csv_out.writerow(("Scope Note",newcon[30:],"| ",newcon.encode("utf-8")," |",litterm.encode("utf-8")," |",newscope.encode("utf-8")," |"))

    if newex == None:
        pass
    else:
        if [newcon.encode("utf-8"),newex.encode("utf-8")] in examplelist:
            pass
        else:
            csv_out.writerow(("Example",newcon[30:],"| ",newcon.encode("utf-8")," |",litterm.encode("utf-8")," |",newex.encode("utf-8")," |"))


#gets removed related links
for a in relatedlist:
    if a in newrelatedlist:
        pass
    else:
        csv_out.writerow(("Removed Related",a[0][30:],"| ",a[0].encode("utf-8")," |",deplit(a[0]).encode("utf-8")," |",a[1].encode("utf-8")," |",deplit(a[1]).encode("utf-8")," |"))

fileout.close()

print "finished!"