# coding: utf-8
## This scripts compares two versions of the UAT and generates
## information such as new concepts, deprecated concepts
## new related links, new alt labels, new pref labels, etc etc.
## Data is useful in creating the release notes

import csv
# import pandas as pd
from datetime import datetime

import rdflib
from rdflib import URIRef

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

w3baseUrl: str = 'https://www.w3.org/2009/08/skos-reference/skos.html#'

#defines certain properties within the SKOS-RDF file
prefLabel: URIRef = rdflib.term.URIRef(w3baseUrl + 'prefLabel')
Concept: URIRef = rdflib.term.URIRef(w3baseUrl + 'Concept')
altLabel: URIRef = rdflib.term.URIRef(w3baseUrl + 'altLabel')
scopenotes: URIRef = rdflib.term.URIRef(w3baseUrl + 'scopeNote')
example: URIRef = rdflib.term.URIRef(w3baseUrl + 'example')
related: URIRef = rdflib.term.URIRef(w3baseUrl + 'related')
definition: URIRef = rdflib.term.URIRef(w3baseUrl + 'definition')
label: URIRef = rdflib.term.URIRef('https://www.w3.org/2000/01/rdf-schema#label')

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


with open('release_note_helper_'+timestamp+'.csv','w', encoding='utf-8', newline='') as fileout:

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

            if oldalts is None or newalts is None:
                pass

            else:
                for x in newalts:
                    if x in oldalts:
                        copynewalts.remove(x)

                for y in oldalts:
                    if y in newalts:
                        copyoldalts.remove(y)

            if copyoldalts is not None and copyoldalts != []:
                aoldalts = ", ".join(copyoldalts)
                wr.writerow((["Removed Alts"]+[newcon[30:]]+["| "]+[newcon]+[" | "]+[lit(newcon)]+[" | "]+[aoldalts]+[" |"]))

            if copynewalts is not None and copynewalts != []:
                anewalts = ", ".join(copynewalts)
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
            if morealts is not None:
                amorealts = ", ".join(morealts)
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
        if rterms is not None:
            for x in rterms:
                littermx = lit(x)
                relatedlist.append([oldcon,x])

    newrelatedlist = []
    for newcon in allnewconcepts:
        litterm = lit(newcon)
        rterms = getrelatedterms(newcon,g)
        if rterms is not None:
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

        if olddef is not None:
            deflist.append([oldcon,olddef])

        if oldscope is not None:
            scopelist.append([oldcon,oldscope])

        if oldex is not None:
            examplelist.append([oldcon,oldex])

    for newcon in allnewconcepts:
        newdef = getdefinition(newcon,g)
        newscope = getscopenotes(newcon,g)
        newex = getexample(newcon,g)
        litterm = lit(newcon)

        if newdef is not None:
            if [newcon,newdef] not in deflist:
                wr.writerow(("Definition",newcon[30:],"| ",newcon," | ",litterm," | ",newdef," |"))

        if newscope is not None:
            if [newcon,newscope] in scopelist:
                pass
            else:
                wr.writerow(("Scope Note",newcon[30:],"| ",newcon," | ",litterm," | ",newscope," |"))

        if newex:
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

print ("finished!")