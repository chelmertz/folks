#!/usr/bin/env python

from setuptools import setup

VERSION = '0.1.0'

setup(
    author='Carl Helmertz',
    author_email='helmertz@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console'
    ],
    description='Manage contacts via CLI',
    entry_points={
        'console_scripts': [
            'folks = folks:main'
        ]
    },
    long_description=open('README').read(),
    name='folks',
    py_modules=['folks'],
    url='https://github.com/chelmertz/folks',
    version=VERSION
)
