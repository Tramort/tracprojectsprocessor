#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = '0.1'
PACKAGE = 'projectsprocessor'

setup(
    name='ProjectsProcessorMacro',
    version=VERSION,
    description="Lists projects based on a name.",
    url='http://fsz-trac/wiki/ProjectsProcessorMacro',
    author='Max "Jake" Kaskevich',
    author_email='maxim.kaskevich@gmail.com',
    keywords='trac plugin',
    license="?",
    packages=[PACKAGE],
    include_package_data=True,
    package_data={},
    install_requires=[],
    zip_safe=False,
    entry_points={
        'trac.plugins': '%s = %s.macro' % (PACKAGE, PACKAGE),
    },
)
