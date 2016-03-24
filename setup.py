# -*- coding: utf-8 -*-
# flake8: noqa

"""Installation script."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os
import os.path as op
import re

from setuptools import setup


#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

def _package_tree(pkgroot):
    path = op.dirname(__file__)
    subdirs = [op.relpath(i[0], path).replace(op.sep, '.')
               for i in os.walk(op.join(path, pkgroot))
               if '__init__.py' in i[2]]
    return subdirs


curdir = op.dirname(op.realpath(__file__))
readme = open(op.join(curdir, 'README.md')).read()


# Find version number from `__init__.py` without executing it.
filename = op.join(curdir, 'phycontrib/__init__.py')
with open(filename, 'r') as f:
    version = re.search(r"__version__ = '([^']+)'", f.read()).group(1)


setup(
    name='phycontrib',
    version=version,
    license="BSD",
    description='Spike sorting and ephys data analysis '
                'for 1000 channels and beyond',
    long_description=readme,
    author='Kwik Team',
    author_email='cyrille.rossant at gmail.com',
    url='https://phy.cortexlab.net',
    packages=_package_tree('phycontrib'),
    package_dir={'phycontrib': 'phycontrib'},
    package_data={
        'phycontrib': ['*.npy', '*.gz', '*.txt', '*.json', '*.prb'],
    },
    include_package_data=True,
    keywords='phy,data analysis,electrophysiology,neuroscience',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Framework :: IPython",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)


def _create_loader_file():
    """Create a Python script that imports phycontrib in the
    plugins directory. This ensures that phycontrib's plugins are always
    loaded by phy."""
    # Make sure the plugins directory exists.
    plugins_dir = op.expanduser('~/.phy/plugins/')
    if not op.exists(plugins_dir):
        os.makedirs(plugins_dir)
    # Create the script if it doesn't already exist.
    path = plugins_dir + 'phycontrib_loader.py'
    if op.exists(path):
        return
    with open(path, 'w') as f:
        f.write(dedent("""
                # Automatically generated by phycontrib's installer.
                # This imports all of phycontrib's plugins when loading phy.
                import phycontrib
                """).lstrip())


# Create ~/.phy/plugins/phycontrib_loader.py.
_create_loader_file()
