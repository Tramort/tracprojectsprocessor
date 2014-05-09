# -*- coding: utf-8 -*-
"""Adds a wiki macro [[Projects]] which lists projects, and links to wiki pages
describing the projects in more detail, and any tickets for the projects. Adds
a wiki macro [[Components]] which lists and describes the project's components,
and links to wiki pages describing the components in more detail, and any
tickets for the components.  The optional project_filter parameter is a regex
that can be used to filter components by project name.
Work only with http://trac-hacks.org/wiki/SimpleMultiProjectPlugin .
Based on http://trac-hacks.org/wiki/ComponentsProcessorMacro ,
thanks to terry_n_brown@yahoo.com

maxim.kaskevich@gmail.com
"""

import inspect
import sys
import re

from trac.core import Component, implements
from trac.wiki.api import IWikiMacroProvider
from trac.wiki import format_to_html


class ProjectsProcessor(Component):
    implements(IWikiMacroProvider)

    # IWikiMacroProvider interface

    def get_macros(self):
        yield 'Projects'

    def get_macro_description(self, name):
        return inspect.getdoc(sys.modules.get(self.__module__))

    def expand_macro(self, formatter, name, args):

        cursor = self.env.get_db_cnx().cursor()

        query = "SELECT id_project, name, description from smp_project order by name;"
        cursor.execute(query)

        projs = [proj for proj in cursor]

        # get a distinct list of all projects for which there are tickets
        query = "SELECT value from ticket_custom WHERE name='project'"
        cursor.execute(query)
        tickets = [page[0] for page in cursor]

        content = []

        for id_project, name, descrip in projs:
            
            # Get number of tickets
            count = 0
            query = "SELECT count(ticket) FROM ticket_custom WHERE value='%s' AND name='project'" % name
            cursor.execute(query)
            for count, in cursor:
                break
            
            p = re.compile(' ')
            dt = ' [wiki:"%s" %s]' % (name, name)
            if name in tickets:
                dt += ' ([query:"project=%s" %d tickets])' % (name, count)
            dt += '::'
            content.append(dt)
            if descrip != None and descrip.strip() != '':
                content.append('   %s' % descrip)

        content = '\n'.join(content)

        content = format_to_html(self.env, formatter.context, content)
        p = re.compile('%2B')
        content = p.sub('+',content)
        content = '<div class="component-list">%s</div>' % content

        return content

class ComponentsProcessor(Component):
    implements(IWikiMacroProvider)

    # IWikiMacroProvider interface

    def get_macros(self):
        yield 'Components'

    def get_macro_description(self, name):
        return inspect.getdoc(sys.modules.get(self.__module__))

    def expand_macro(self, formatter, name, project_filter):

        cursor = self.env.get_db_cnx().cursor()

        query = "SELECT name, description from component order by name;"
        cursor.execute(query)

        comps = [comp for comp in cursor]

        # get a distinct list of all components for which there are tickets
        query = "SELECT component from ticket group by component;"
        cursor.execute(query)
        tickets = [page[0] for page in cursor]

        content = []

        components = []
        if project_filter:
            query = """SELECT
                        m.component AS component
                   FROM
                        smp_project AS p,
                        smp_component_project AS m
                   WHERE
                        p.name = %s AND
                        p.id_project = m.id_project"""
            cursor.execute(query, [project_filter])
            components = [x[0] for x in cursor.fetchall()]


        for name, descrip in comps:
            if project_filter and not name in components:
                continue
            
            # Get number of tickets
            count = 0
            query = "SELECT count(id) FROM ticket WHERE component='%s'" % name
            cursor.execute(query)
            for count, in cursor:
                break
            
            p = re.compile(' ')
            ticket_str = p.sub('+',name)
            dt = ' [wiki:"%s" %s]' % (name, name)
            if name in tickets:
                dt += ' ([query:component=%s %d tickets])' % (ticket_str, count)
            dt += '::'
            content.append(dt)
            if descrip != None and descrip.strip() != '':
                content.append('   %s' % descrip)

        content = '\n'.join(content)

        content = format_to_html(self.env, formatter.context, content)
        p = re.compile('%2B')
        content = p.sub('+',content)
        content = '<div class="component-list">%s</div>' % content

        # to avoid things like the above it might be nicer to use
        # Genshi tag() construction, but this way the wiki formatter
        # gets to deal with '[query:component=%s tickets]' etc.
        # if going the Genshi route you'd replace that with something
        # like req.href.query(component="mycomp", status="open")

        return content
