# coding: utf-8

# deprecated concepts
## use instead
# alt labels


print ("You can ignore the UnicodeWarning if you get one...")

#Alex's script
flat_j = {}

for t in allconcepts:

    if getdepstatus(t) == None: # if concept is NOT deprecated
        litt = (lit(t))
        
        p = getbroaderterms(t)
        c = getnarrowerterms(t)
        alts = getaltterms(t)
     
        pl = []
        rcl = []
        
        if p == None:
            pl = ["astro_thes"]
        else:
            for x in p:
                y = (lit(x))
                pl.append(y)

        if c == None:
            pass
        else:
            for x in c:
                y = (lit(x))
                rcl.append(y)

        rts = getrelatedterms(t)
        rtlist = []
        if rts != None:
            for rt in rts:
                urt = {}
                urt["name"] = lit(rt)
                urt["uri"] = rt
                rtlist.append(urt)
            #onecon["related"] = rtlist
        else: 
            rtlist = None

        # onecon["changeNotes"] = getchangenotes(t)
        # onecon["scopeNotes"] = getscopenotes(t)
        # onecon["examples"] = getexample(t)
        # onecon["definition"] = getdefinition(t)
        # onecon["editorialNotes"] = getednotes(t)
     
        flat_j[litt] = {

            "parents" : pl,
            "children" : [],
            "real_children": rcl,
            "uri": t,
            "altLabels" : alts,
            "related" : rtlist,
            "changeNotes" : getchangenotes(t),
            "scopeNotes" : getscopenotes(t),
            "examples" : getexample(t),
            "definition" : getdefinition(t),
            "editorialNotes" : getednotes(t),
        }

    # if alts != None:
    #     flat_j[litt]["altLabels"] = alts

#print (flat_j)


def recurse_traverse(info_dict, name_of_dict, flat_j):
    #step one: add all entries from flat_j to children dict that have parents that equal the key name from the dict
    for f in flat_j:
        #print (f)

        if name_of_dict in flat_j[f]["parents"]:
            info_dict["children"].append({
                "name"          : f,
                "uri"           : flat_j[f]["uri"],
                "altLabels"     : flat_j[f]["altLabels"],
                "related"       : flat_j[f]["related"],
                "changeNotes"   : flat_j[f]["changeNotes"],
                "scopeNotes"    : flat_j[f]["scopeNotes"],
                "examples"      : flat_j[f]["examples"],
                "definition"    : flat_j[f]["definition"],
                "editorialNotes": flat_j[f]["editorialNotes"],
                "children"      :[],
                })
    #step two: now that the entries are added, repeat the process on each of them. A full path to that 
    #child within the original "info_dict" becomes the new info_dict. If there were no entries added
    #to children, this will throw a key error, so we stop recursing on this branch
    if len(info_dict["children"])>0:
        #print len(info_dict["children"])
        #print info_dict["children"]
        children_dict = info_dict["children"]
        #print(children_dict)
        #children_dict.sort(); #sorts child terms alphabetically
        children_dict.sort(key=lambda item: item.get("name"))
        for i, child_dict in enumerate(children_dict):  
            recurse_traverse(children_dict[i], child_dict["name"], flat_j)
    else:
        del info_dict["children"]


astro_thes = {"children":[]}

print ("It might be a long pause here as it loops through the UAT...")
recurse_traverse(astro_thes, "astro_thes", flat_j)

#print (astro_thes)

alldep = []

for t in alldepconcepts:

    onecon = {}
    onecon["uri"] = t
    onecon["name"] = getlabel(t)
    onecon["status"] = "deprecated"
    

    chnote = getchangenotes(t)
    uselist = []
    if chnote != None:
        for x in chnote:
            if str(x["title"]) == 'Use instead':
                uselist.append(x["comment"])

        onecon["useInstead"] = uselist

    alldep.append(onecon)



astro_thes["deprecated"] = alldep

#print (astro_thes)

#all uat in one file
js_file = open("uat_"+timestamp+".json", "w")
js_file.write(json.dumps(astro_thes))

js_file.close()


# #seperate file for each top concept
# for x in astro_thes["children"]:
#     tc = x["name"]
#     js_file1 = open("uat_"+tc+"_"+timestamp+".json", "wb")
#     js_file1.write(json.dumps(x))
#     js_file1.close()