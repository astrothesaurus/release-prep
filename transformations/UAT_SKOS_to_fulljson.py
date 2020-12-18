# coding: utf-8


print ("Writing web json file...")

alluat = []
#writes an html file for each term
for t in allconcepts:
    #urlterm = unicode(lit(t)).replace(" ", "+").replace("/", "_")
    #get all the info for each term
    onecon = {}
    onecon["uri"] = t
    onecon["name"] = lit(t)
    
    nts = getnarrowerterms(t)
    ntlist = []
    if nts != None:
        for nt in nts:
            unt = {}
            unt["name"] = lit(nt)
            unt["uri"] = nt
            ntlist.append(unt)
        onecon["narrower"] = ntlist
    else: 
        onecon["narrower"] = nts
    
    bts = getbroaderterms(t)
    btlist = []
    if bts != None:
        for bt in bts:
            ubt = {}
            ubt["name"] = lit(bt)
            ubt["uri"] = bt
            btlist.append(ubt)
        onecon["broader"] = btlist
    else: 
        onecon["broader"] = bts

    ats = getaltterms(t)
    onecon["altNames"] = ats

    rts = getrelatedterms(t)
    rtlist = []
    if rts != None:
        for rt in rts:
            urt = {}
            urt["name"] = lit(rt)
            urt["uri"] = rt
            rtlist.append(urt)
        onecon["related"] = rtlist
    else: 
        onecon["related"] = rts

    onecon["changeNotes"] = getchangenotes(t)
    onecon["scopeNotes"] = getscopenotes(t)
    onecon["examples"] = getexample(t)
    onecon["definition"] = getdefinition(t)
    onecon["editorialNotes"] = getednotes(t)

    alluat.append(onecon)



for t in alldepconcepts:

    onecon = {}
    onecon["uri"] = t
    onecon["name"] = getlabel(t)
    onecon["status"] = "deprecated"
    

    chnote = getchangenotes(t)
    print (chnote)
    uselist = []
    if chnote != None:
        for x in chnote:
            if x["title"] == rdflib.term.Literal('Use instead'):
                uselist.append(x["comment"])

        onecon["useInstead"] = uselist

    alluat.append(onecon)



#all uat in one file
js_file = open("uat_list"+timestamp+".json", "w")
js_file.write(json.dumps(alluat))

js_file.close()

print ("Finished.")