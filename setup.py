#!/usr/bin/env python

import os
from setuptools import find_packages, setup
from pip.req import parse_requirements

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements/base.txt', session=False)
# e.g. ['suds==0.4']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='publish_eccu',
    version='0.0.1',
    author='CFPB',
    author_email='emmanuel.apau@cfpb.gov',
    packages=find_packages(),
    include_package_data=True,
    description=u'Publish ECCU files to Akamai',
    license='Public Domain, CC0',
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=README,
    test_suite="runtests.runtests",
    zip_safe=False,
    setup_requires=['pbr'],
    pbr=True,
    install_requires=reqs,
)
