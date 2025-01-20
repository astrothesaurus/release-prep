# coding: utf-8


print ("Writing web json file...")

alluat = []
#writes an html file for each term
for t in allconcepts:
    #urlterm = unicode(lit(t)).replace(" ", "+").replace("/", "_")
    #get all the info for each term

    if getdepstatus(t) is None: # if concept is NOT deprecated
        onecon = {"id": int(t[30:]), "concept": lit(t), "ednotes": getednotes(t), "chnotes": getchangenotes(t),
                  "scnotes": getscopenotes(t), "examples": getexample(t), "defnote": getdefinition(t)}

        #vocstats = getvocstatus(t)

        #print(getdefinition(t))

        nts = getnarrowerterms(t)
        ntlist = []
        if nts is not None:
            for nt in nts:
                unt = {"concept": lit(nt), "id": int(nt[30:])}
                ntlist.append(unt)
            onecon["narrower"] = ntlist
        else: 
            onecon["narrower"] = nts
        
        bts = getbroaderterms(t)
        btlist = []
        if bts is not None:
            for bt in bts:
                ubt = {"concept": lit(bt), "id": int(bt[30:])}
                btlist.append(ubt)
            onecon["broader"] = btlist
        else: 
            onecon["broader"] = bts

        ats = getaltterms(t)
        onecon["alts"] = ats

        rts = getrelatedterms(t)
        rtlist = []
        if rts is not None:
            for rt in rts:
                urt = {"concept": lit(rt), "id": int(rt[30:])}
                rtlist.append(urt)
            onecon["related"] = rtlist
        else: 
            onecon["related"] = rts

        alluat.append(onecon)


#all uat in one file
with open("uat_list_webjson"+timestamp+".json", "w") as js_file:
    js_file.write(json.dumps(alluat))

print ("Finished.")