tracprojectsprocessor
==============

Simple trac(http://trac.edgewall.org/) plugin.

Adds a wiki macro [[Projects]] which lists projects, and links to wiki pages
describing the projects in more detail, and any tickets for the projects. Adds
a wiki macro [[Components]] which lists and describes the project's components,
and links to wiki pages describing the components in more detail, and any
tickets for the components.  The optional project_filter parameter is a regex
that can be used to filter components by project name.
Work only with http://trac-hacks.org/wiki/SimpleMultiProjectPlugin .
Based on http://trac-hacks.org/wiki/ComponentsProcessorMacro ,
thanks to terry_n_brown@yahoo.com

maxim.kaskevich@gmail.com

Installation
------------------------

1. build egg:
 - `git clone --progress -v "https://github.com/Tramort/tracprojectsprocessor.git" "tracprojectsprocessor"`
 - `cd tracprojectsprocessor`
 - `python setup.py bdist_egg`

2. copy egg file from "tracprojectsprocessor/dist" to "plugins" dir in trac enviroment
