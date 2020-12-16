# coding: utf-8


print ("Writing web json file...")

alluat = []
#writes an html file for each term
for t in allconcepts:
    #urlterm = unicode(lit(t)).replace(" ", "+").replace("/", "_")
    #get all the info for each term
    onecon = {}
    onecon["id"] = int(t[30:])
    onecon["concept"] = lit(t)
    
    #vocstats = getvocstatus(t)
    onecon["ednotes"] = getednotes(t)
    onecon["chnotes"] = getchangenotes(t)
    onecon["scnotes"] = getscopenotes(t)
    onecon["exnotes"] = getexample(t)
    onecon["defnote"] = getdefinition(t)

    nts = getnarrowerterms(t)
    ntlist = []
    if nts != None:
        for nt in nts:
            unt = {}
            unt["concept"] = lit(nt)
            unt["id"] = int(nt[30:])
            ntlist.append(unt)
        onecon["narrower"] = ntlist
    else: 
        onecon["narrower"] = nts
    
    bts = getbroaderterms(t)
    btlist = []
    if bts != None:
        for bt in bts:
            ubt = {}
            ubt["concept"] = lit(bt)
            ubt["id"] = int(bt[30:])
            btlist.append(ubt)
        onecon["broader"] = btlist
    else: 
        onecon["broader"] = bts

    ats = getaltterms(t)
    onecon["alts"] = ats

    rts = getrelatedterms(t)
    rtlist = []
    if rts != None:
        for rt in rts:
            urt = {}
            urt["concept"] = lit(rt)
            urt["id"] = int(rt[30:])
            rtlist.append(urt)
        onecon["related"] = rtlist
    else: 
        onecon["related"] = rts

    alluat.append(onecon)


#all uat in one file
js_file = open("uat_list"+timestamp+".json", "w")
js_file.write(json.dumps(alluat))

js_file.close()

print ("Finished.")