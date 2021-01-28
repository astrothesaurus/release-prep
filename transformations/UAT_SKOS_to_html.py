# coding: utf-8

print ("Writing term record files...")
directory = 'termrecords'
if os.path.exists(directory):
    shutil.rmtree(directory)
os.makedirs(directory)

#writes an html file for each term
for t in allconcepts:
    urlterm = lit(t).replace(" ", "+").replace("/", "_")
    #get all the info for each term
    print (t)
    usnts = getnarrowerterms(t)
    usbts = getbroaderterms(t)
    usats = getaltterms(t)
    usrts = getrelatedterms(t)
    vocstats = getvocstatus(t)
    ednotations = getednotes(t)
    chnotations = getchangenotes(t)
    scnotations = getscopenotes(t)
    termexample = getexample(t)
    defs = getdefinition(t)

    #create file for this particular term
    fileterm = open("termrecords\\"+urlterm+".html", 'w', encoding='utf-8')
    
    #file header
    fileterm.write("<html>\n")
    fileterm.write("<head><title>Concept Record: "+lit(t)+"</title>\n")
    fileterm.write("<style>a,a:link,a:visited{color:#b4083a;text-decoration:underline}a:hover,a:active{text-decoration:none}a.tooltips,a.figure{color:#b4083a;font-weight:bold;text-decoration:none}h3{padding:0px; margin:0px;display:inline}</style>\n")
    fileterm.write("<meta charset='utf-8'></head>\n<body>\n")
    
    #term heading
    fileterm.write("<h3>"+lit(t)+"</h3>\n")
    fileterm.write("<br/><a target='blank' style='font-size:80%;' href='"+t+"'>"+t+"</a>\n")
    
    #broader terms
    if usbts != None:
        fileterm.write("<dl>\n<p><dt><i>Broader Concept(s)</i>:</dt>\n")
        usbt = []
        for ubt in usbts:
            usbt.append(lit(ubt))
        sbt = sorted(usbt)
        for bt in sbt:
            bturl = bt.replace(" ", "+").replace("/", "")+".html"
            cbturl = bturl
            if bt in deprecated:
                fileterm.write("<dd><del><a href=\""+cbturl+"\">"+bt+"</a></del></dd>\n")
            else:
                fileterm.write("<dd><a href=\""+cbturl+"\">"+bt+"</a></dd>\n")
        fileterm.write("</p>\n")
    else:
        fileterm.write("<br /><br/><a href='toplevelconcepts.html'>view all top level concepts</a>\n") 
    
    #narrower terms
    if usnts != None:
        fileterm.write("<p><dt><i>Narrower Concept(s)</i>:</dt>\n")
        usnt = []
        dusnt = []
        for unt in usnts:
            usnt.append(lit(unt))
        snt = sorted(usnt)
        for nt in snt:
            nturl = nt.replace(" ", "+").replace("/", "")+".html"
            cnturl = nturl
            if nt in deprecated:
                fileterm.write("<dd><del><a href=\""+cnturl+"\">"+nt+"</a></del></dd>\n")
            else:           
                fileterm.write("<dd><a href=\""+cnturl+"\">"+nt+"</a></dd>\n")
        fileterm.write("</p>\n")
    
    #related terms
    if usrts != None:
        fileterm.write("<p><dt><i>Related Concept(s)</i>:</dt>\n")
        usrt = []
        for urt in usrts:
            usrt.append(lit(urt))
        srt = sorted(usrt)
        for rt in srt:
            rturl = rt.replace(" ", "+").replace("/", "")+".html"
            crturl = rturl
            if rt in deprecated:
                fileterm.write("<dd><del><a href=\""+crturl+"\">"+rt+"</a></del></dd>\n")
            else:
                fileterm.write("<dd><a href=\""+crturl+"\">"+rt+"</a></dd>\n")
        fileterm.write("</p>\n")

    #alternate forms
    if usats != None:
        fileterm.write("<p><dt><i>Use For</i>:</dt>\n")
        usat = []
        for at in usats:
            #usat.append(getaltterms(uat))
        #sat = sorted(usat)
        #for at in sat:
            print (at)
            fileterm.write("<dd>"+at+"</dd>\n")
        fileterm.write("</p>\n")

    #definitions
    if defs != None:
        fileterm.write("<p><dt><i>Definition</i>:</dt>\n")

        if ednotations != None:
            for x in ednotations:
                print(x)
                if x["title"] == rdflib.term.Literal('Definition Provenance'):
                    print ("yes")
                    source = x["comment"]
        
                    fileterm.write("<dd>"+defs+"<br/>&nbsp;&nbsp;&nbsp;&nbsp; - <cite>"+source+"</cite></dd>\n")
                else:
                    print("no")
        else:
            fileterm.write("<dd>"+defs+"</dd>\n")

        fileterm.write("</p>\n")



    #examples
    if termexample != None:
        fileterm.write("<p><dt><i>Examples</i>:</dt>\n")
        fileterm.write("<dd>"+termexample+"</dd>\n")
        fileterm.write("</p>\n")

    #editorial notes
    if ednotations != None:
        print (ednotations)
        # fileterm.write("<p><dt><i>Editorial Notes</i>:</dt>\n")
        # fileterm.write("<dd>"+ednotations+"</dd>\n")
        # fileterm.write("</p>\n")

    #change notes
    if chnotations != None:
        print (chnotations)
        # fileterm.write("<p><dt><i>Change Notes</i>:</dt>\n")
        # fileterm.write("<dd>"+chnotations+"</dd>\n")
        # fileterm.write("</p>\n")

    #scope notes
    if scnotations != None:
        fileterm.write("<p><dt><i>Scope Notes</i>:</dt>\n")
        fileterm.write("<dd>"+scnotations+"</dd>\n")
        fileterm.write("</p>\n")
   
    #status
    if vocstats != None:
        fileterm.write("<p><dt><i>Status</i>:</dt>\n")
        fileterm.write("<dd>"+vocstats+"</dd></p>\n")
        
    #finish off html and close file
    fileterm.write("</dl>\n")
    fileterm.write("</body>\n</html>\n")
    fileterm.close()

print ("Writing toplevelconcepts.html...")
#creates toplevelconcepts.html
filetop = open("termrecords\\toplevelconcepts.html", 'w', encoding='utf-8')
filetop.write("<html>\n")
filetop.write("<head><title>Top Level Concepts</title>\n")
filetop.write("<style>a,a:link,a:visited{color:#b4083a;text-decoration:underline}a:hover,a:active{text-decoration:none}a.tooltips,a.figure{color:#b4083a;font-weight:bold;text-decoration:none}</style>\n")
filetop.write("<meta charset='utf-8'></head>\n<body>\n")
filetop.write("<h3>UAT Top Level Concepts</h3>\n")
ust = []
for ut in alltopconcepts:
    ust.append(lit(ut))
st = sorted(ust)
for t in st:
    urlterm = t.replace(" ", "+").replace("/", "_")
    curlterm = urlterm
    if t in deprecated:
        filetop.write("<del><a href=\""+curlterm+".html\">"+t+"</a></del></br>\n")
    else:
        filetop.write("<a href=\""+curlterm+".html\">"+t+"</a></br>\n")
filetop.write("</body>\n</html>\n")
filetop.close()

print ("Writing alphaleft.html...")
#creates alphabetial list of terms with first letter headers.
filealpha = open("alphaleft.html", 'w', encoding='utf-8')
filealpha.write("<html>\n")
filealpha.write("<head>\n")
#next line includes autocomplete script and faux searchbar
filealpha.write("<script src='https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js'></script>\n<script src='https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js'></script>\n<link rel='stylesheet' href='https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/smoothness/jquery-ui.min.css' id='rel'>\n<script src='https://wolba.ch/astrothesaurus/uat/uat_autocomplete.js'></script>\n")
filealpha.write("<title>UAT Alphabetical List</title>\n")
filealpha.write("<style>f html,body,div,span,applet,object,iframe,h1,h2,h3,h4,h5,h6,p,blockquote,pre,a,abbr,acronym,address,big,cite,code,del,dfn,font,img,ins,kbd,q,s,samp,small,strike,sub,sup,tt,var,dl,dt,dd,ol,ul,li,fieldset,form,label,legend,table,caption,tbody,tfoot,thead,tr,th,td{margin:0;margin-top:0;padding:0;border:0;outline:0;font-weight:inherit;font-style:inherit;font-size:100%;font-family:inherit;vertical-align:baseline}html{font-size:100.01%}body{font-family:Arial,Tahoma,Verdana;font-size:0.9em;border:0;color:#222}ul,ol{list-style:none}img{border:none}.clear{clear:both}a,a:link,a:visited{color:#24041b;text-decoration:underline}a:hover,a:active{text-decoration:none}input,textarea{background-color:#f5f5f5;margin:5px;border-top:1px solid #eee;border-left:1px solid #eee;border-right:1px solid #ddd;border-bottom:1px solid #ddd;color:#333}#navi{float:left;width:890px;margin-top:0px;padding:0 5px;background:#24041b;font-family:Arial,Tahoma,Verdana}#nav,#nav ul{margin:0;padding:0;list-style-type:none;list-style-position:outside;position:relative}#nav li{float:left;position:relative}#nav a{display:block;padding:3px 15px;margin:7px 0;font-size:1em;font-weight:bold;text-decoration:none;color:#fff;border-right:1px solid #fff}#nav a:link,#nav a:visited{text-decoration:none}#nav a:hover{color:#24041b;background:#eee}#nav ul{position:absolute;display:none;z-index:99;border-top:1px solid #ccc}#nav ul a{width:180px;padding:10px;margin:0;float:left;color:#333;font-size:0.9em;background:#fff;border-top:none;border-left:2px solid #aaa;border-right:1px solid #bbb;border-bottom:1px solid #ccc}#nav ul a:hover{color:#444!important;background:#e0e0e0}#nav ul ul{margin-top:-1px;padding-left:2px}#nav li ul ul{margin-left:200px}#nav li:hover ul ul,#nav li:hover ul ul ul,#nav li:hover ul ul ul ul{display:none}#nav li:hover ul,#nav li li:hover ul,#nav li li li:hover ul,#nav li li li li:hover ul{display:block}</style>\n")
filealpha.write("<meta charset='utf-8'></head>\n<body>\n")
filealpha.write('<form name="testing1">\n<input type="text" id="uat-autocomplete-single" name="uatterm1"> <INPUT TYPE="button" value="Search" onClick="parent.rightframe.location=\'https://wolba.ch/astrothesaurus/uat/termrecords/\' + uatterm1.value.split(\' \').join(\'+\') + \'.html\'">\n</form>\n')

usac = []
for usc in allconcepts:
    usac.append(lit(usc))
sac = sorted(usac, key=lambda s: s.lower())
previous = None  
for c in sac:
    if previous != c[0].lower():
        previous = c[0].lower()
        filealpha.write("<br /><b><a id='"+c[0]+"'>"+c[0]+"</a></b><br/><br/>")
    urlterm = c.replace(" ", "+").replace("/", "_")
    curl = urlterm
    if c in deprecated:
        filealpha.write("<del><a href=\"termrecords/"+curl+".html\" target='rightframe'>"+c+"</a></del></br>\n")
    else:
        filealpha.write("<a href=\"termrecords/"+curl+".html\" target='rightframe'>"+c+"</a></br>\n")
#next line for autocomplete script and faux searchbar
filealpha.write('</body>\n<script>\n$("#uat-autocomplete-single").uatAutocomplete()\n\n$("#uat-autocomplete-multi").uatAutocomplete({\n    multi: true\n})\n</script>\n')

filealpha.write("</html>\n")
filealpha.close()

#returns a sorted list of terms, used for the alphabetical browser
def sortlist(unsortedlist):
    ustl = []
    sl = []
    for t in unsortedlist:
        ustl.append(lit(t))
    x = sorted(ustl)
    for s in x:
        for n in g.subjects(predicate=prefLabel, object=s):
 
            sl.append(n)
    return sl

#builds the formatted list of terms for the hierarchy browser
def buildlist(termlist, filename):
    for xt in sortlist(termlist):
        xtr = lit(xt)
        urlxt = xtr.replace(" ", "+").replace("/", "_")
        if xtr in deprecated:
            filename.write("<li><del><a target='basefrm' href=\"termrecords/"+urlxt+".html\">"+lit(xt)+"</a></del>")
        else:
            filename.write("<li><a target='basefrm' href=\"termrecords/"+urlxt+".html\">"+lit(xt)+"</a>")
        yt = getnarrowerterms(xt)
        if yt != None:
            filename.write("\n<ul class='treeview'>\n")
            buildlist(yt, filename)
        if yt == None:
            filename.write("</li>\n")
    filename.write("</ul></li>\n")

print ("Writing tree.html...")
filetree = open("tree.html", 'w', encoding='utf-8')
filetree.write("<html>\n")
filetree.write("<head>\n<title>UAT Hierarchy Tree View</title>\n")
filetree.write("<script type='text/javascript' src='simpletreemenu.js'>\n")
filetree.write("/***********************************************\n")
filetree.write("* Simple Tree Menu- © Dynamic Drive DHTML code library (www.dynamicdrive.com)\n")
filetree.write("* This notice MUST stay intact for legal use\n")
filetree.write("* Visit Dynamic Drive at http://www.dynamicdrive.com/ for full source code\n")
filetree.write("***********************************************/\n")
filetree.write("</script>\n")
filetree.write("<link rel='stylesheet' type='text/css' href='simpletree.css' />\n")
filetree.write("<meta charset='utf-8'></head>\n<body>\n")
filetree.write("</head>\n")
filetree.write("</body>\n")
filetree.write("<h4>Unified Astronomy Thesaurus</h4>\n")
filetree.write("<div class='advmenu'>\n")
filetree.write("<a href=\"javascript:ddtreemenu.flatten('treemenu1', 'expand')\">expand all</a> | <a href=\"javascript:ddtreemenu.flatten('treemenu1', 'collapse')\">collapse all</a>\n")
filetree.write("</div>\n")
filetree.write("<ul id='treemenu1' class='treeview'>\n")

buildlist(alltopconcepts, filetree)

filetree.write("<script type='text/javascript'>\n")
filetree.write("//ddtreemenu.createTree(treeid, enablepersist, opt_persist_in_days (default is 1))\n")
filetree.write("ddtreemenu.createTree('treemenu1', false)\n")
filetree.write("</script>\n")
filetree.write("</body>\n</html>")

filetree.close()

print ("Finished. See toplevelconcepts.html, alphaleft.html, tree.html, and the termrecords folder")