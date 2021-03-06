#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Thomas Chiroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/lgpl-3.0.html>
#
"""global setup
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import os
import sys

# local imports
from build_scripts.version import get_git_version

if not hasattr(sys, 'version_info') or sys.version_info < (2, 6, 0, 'final'):
    raise SystemExit("xmlpylighter requires Python 2.6 or later.")

with open("README.rst") as f:
    README = f.read()

with open("NEWS.rst") as f:
    NEWS = f.read()

VERSION = None
try:
    VERSION = get_git_version()
except:
    VERSION = None

if VERSION is None:
    try:
        file_name = "src/xmlpylighter/RELEASE-VERSION"
        version_file = open(file_name, "r")
        try:
            VERSION = version_file.readlines()[0]
            VERSION = VERSION.strip()
        except:
            VERSION = "0.0.0"
        finally:
            version_file.close()
    except IOError:
        VERSION = "0.0.0"


class my_build_py(build_py):
    def run(self):
        # honor the --dry-run flag
        if not self.dry_run:
            target_dirs = []
            target_dirs.append(os.path.join(self.build_lib, 'xmlpylighter'))
            target_dirs.append('src/xmlpylighter')

            # mkpath is a distutils helper to create directories
            for dir in target_dirs:
                self.mkpath(dir)

            try:
                for dir in target_dirs:
                    fobj = open(os.path.join(dir, 'RELEASE-VERSION'), 'w')
                    fobj.write(VERSION)
                    fobj.close()
            except:
                pass

        # distutils uses old-style classes, so no super()
        build_py.run(self)


install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'bottle',
    'pygments',
    'lxml', ]

try:
    import argparse  # NOQA
except ImportError:
    install_requires.append('argparse')

setup(name='xmlpylighter',
      version=VERSION,
      description="xmlpylighter is a tiny web page to pretty print "
                  "and compare xml files ",
      long_description=README + '\n\n' + NEWS,
      cmdclass={'build_py': my_build_py},
      classifiers=[
          # Get strings from
          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7"],
      keywords='xml diff pprint pretty print',
      author='Thomas Chiroux',
      author_email='',
      url='https://github.com/ThomasChiroux/xmlpylighter',
      license='LGPLv3',
      entry_points={
          'console_scripts': ['xmlpylighter = xmlpylighter.xmlpylighter:main', ],
      },
      packages=find_packages('src'),
      package_dir={'': 'src'}, include_package_data=True,
      package_data={'xmlpylighter': ['RELEASE-VERSION', ]},
      zip_safe=False,
      provides=('xmlpylighter', ),
      install_requires=install_requires,
      #test_suite = 'test.run_all_tests.run_all_tests',
      tests_require=['nose', 'coverage', 'unittest2'],
      test_suite='nose.collector',
      extras_require={
          'doc': ["sphinx", ],
          'devel_tools': ["ipython", "pylint", "pep8", "flake8", ],
      },)
