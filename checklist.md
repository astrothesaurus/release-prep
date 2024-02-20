# UAT Release Check List

### One Week Prior to Release (Friday)
* Finalize/close/move remaining issues in open Milestones
* Close Milestones
* Inform stakeholders at EJPress and IoP of pending release
* Open new Milestone

### Week of Release (Monday - Thursday)
* Export UAT RDF from management tool
  * Project > Export > RDF Project Export
  * Format: RDF/XML
  * Thesaurus Data: Concepts, Deprecated Concepots, SKOS Notes 
* Generate updated UAT files (see UAT_transform.py)
  * check that uat-chooser works
  * json for UAT Apps
    * split into top level groups (split_uat_on_top_level_terms.py) for the [sorting tool](http://uat.wolba.ch)
    * UAT_list for browsing and searching interface
  * javascript for @aholachek's [autocomplete widget](http://astrothesaurus.org/thesaurus/autocomplete-widget/)
* Write UAT Release Notes (see release_notes_generator.py)
  * summary notes & full notes
* Prepare and finalize local UAT repo, commit changes
* Update UAT transformation scripts in GitHub if needed
* Select new image for website header rotation
* Write annoucement blog post, schedule for release
* Update this checklist if needed

### Launch Day (Friday)
* Push UAT repo (includes new UAT version, notes, etc) to GitHub
* Upload new json and javascript files to UAT website
* Push new version to UAT API
* Check webtools to make sure everything updated/didn't break:
  * [AAS Journal Submission](http://aas.msubmit.net/)
  * [UAT Concept Selector](http://astrothesaurus.org/concept-select/)
  * [UAT Sorting Tool](https://uat.wolba.ch/sort)
  * [UAT Browse and Search App](https://uat.wolba.ch/uat/)
* Troubleshoot anything that didn't update or is broken
* Update current version number on [UAT homepage](http://astrothesaurus.org/)
* Update current version number on [UAT About Page](https://astrothesaurus.org/about/)
