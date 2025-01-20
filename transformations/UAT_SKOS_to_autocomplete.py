# coding: utf-8

#lists terms and their preferred form in pairs
pl = []
for t in allconcepts:
    if getdepstatus(t) is None: # if concept is NOT deprecated
        litt = lit(t)
        p = getaltterms(t)
        
        flat_j = '{value:"'+litt+'",label:"'+litt+'",uri:"'+t+'"}'
        pl.append(flat_j)

        if p is None:
            pass
        for y in p:
            flat_j1 = '{value:"'+litt+'",label:"'+y+' ('+litt+')'+'",uri:"'+t+'"}'
            pl.append(flat_j1)
            
#joins this list of pairs into a string
q = u','.join(pl).encode('utf-8').strip()

with open("uat_autocomplete.js", "wb") as js_file:

    #opening javascript code, from Alex
    js_file.write(b"(function(b){function a(d){return d.split(/,\s*/)}function c(d){return a(d).pop()}uat_json=[")

    #writes the string of pairs to the file
    js_file.write(q)

    #closing javascript code, from Alex
    js_file.write(b'];b.widget("custom.uatAutocomplete",b.ui.autocomplete,{options:{source:uat_json,multi:false,minLength:3}')
    js_file.write(b',_create:function(){if(this.options.multi===false){this._super()}else{this._super();this.element.bind')
    js_file.write(b'("keydown",function(d){if(d.keyCode===b.ui.keyCode.TAB&&b(this).data("ui-autocomplete").menu.active)')
    js_file.write(b'{d.preventDefault()}}).autocomplete({source:function(e,d){d(b.ui.autocomplete.filter(uat_json,c(e.term)))}')
    js_file.write(b',focus:function(){return false},select:function(e,f){var d=a(this.value);d.pop();d.push(f.item.value);d.push')
    js_file.write(b'("");this.value=d.join(", ");return false}})}}})}(jQuery));')

print ("Finished. See uat_autocomplete.js")