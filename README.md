# mac-ep-office-space
A set of scripts for handling office space at McMaster Engingeering Physics

## Workspace set up

These scripts are made to be run with Python v3.  It is helpful to make a virtual environment for this project using something like:

    mkvirtualenv ep_grads --python=/usr/bin/python3

After this is done and the virtualenv is enabled, be sure to install the required dependencies

    python setup.py install


## parse-grad-students.py

A script to parse the Eng Phys website for all current grad students.

### Run normally

Run the script with

    python parse-grad-students.py

This parses the web site and saves the student data to 'students.csv'

### Debug mode

The debug mode can be enabled with the `-d` flag

    python parse-grad-students.py -d

This looks for a local file `debug.pkl` to parse the HTML from.  If this file does not exist, then the site is parsed and saved to this file.  Useful for testing the script or making changes and not hitting the site over and over again.

### Set the output filename

The file where the formatted data is saved can be set with the `-f` flag

    python parse-grad-students.py -f new_students.csv

Saves the student data to file `new_students.csv`

