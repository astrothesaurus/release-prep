# UAT Release Check List

### Friday Prior to Release
* Finalize/close/move remaining issues in open Milestones
* Close Milestones
* Inform stakeholders at EJPress and IoP of pending release
* Open new Milestone

### Week of Release
* Export UAT RDF from management tool
* Generate updated UAT files (see UAT_transform.py)
  * html for [concept records](http://wolba.ch/astrothesaurus/uat/termrecords) that support [alphabetical](http://wolba.ch/astrothesaurus/uat/alpha.html) and [hierarchical](http://wolba.ch/astrothesaurus/uat/hierarchy.html) browsers
  * json for [sorting tool](http://uat.wolba.ch)
  * javascript for @aholachek's [autocomplete widget](http://astrothesaurus.org/thesaurus/autocomplete-widget/)
* Write UAT Release Notes (see release_notes_generator.py)
  * summary notes & full notes
* Prepare and finalize local UAT repo, commit changes
* Update UAT transformation scripts in GitHub if needed
* Update this checklist if needed
* Select new image for website header rotation

### Launch Day
* Push UAT repo (includes new UAT version, notes, etc) to GitHub
* Upload new html, json, js files to UAT website
* Push new version to UAT API
* Check webtools to make sure everything updated/didn't break:
  * [AAS Journal Submission](http://aas.msubmit.net/)
  * [UAT Sorting Tool](https://uat.wolba.ch/)
  * [UAT Concept Selector](http://astrothesaurus.org/concept-select/)
  * [Alphabetical Browse](http://astrothesaurus.org/thesaurus/alphabetical-browse/)
  * [Hierarchical Browse](http://astrothesaurus.org/thesaurus/hierarchical-browse/)
  * [Autocomplete Widget](http://astrothesaurus.org/thesaurus/autocomplete-widget/)
* Troubleshoot anything that didn't update or is broken
