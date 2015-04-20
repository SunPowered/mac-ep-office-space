#!/usr/bin/env python

from distutils.core import setup

setup(name="Eng Phys Office Space Tools",
      description="A set of scripts to work with the Eng Phys office space committee",
      version="0.1dev",
      author="Tim van Boxtel",
      author_email="vanboxtj@mcmaster.ca",
      py_modules=['parse-grad-students'],
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT",
      ],
      requires=['bs4 (>=4.3.2)',
                'requests (>=2.6.0)']),

