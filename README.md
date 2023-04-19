# Workshop Web Home Space
This is a web application that allows users to explore and navigate their own home directoy, search for files, and view their contents.

## Features
+ User authentication: users can log in, and log out. (based on /etc/shadow)
+ File navigation: users can navigate their file system, view directories and files in the current directory.
+ File search: users can search for files by name or extension.
+ File viewing: users can view the contents of text files in the browser.
+ File download: users can download their home directory from the server.

## Technologies
+ Backend: Python Flask
+ Frontend: HTML, CSS and Jinja2

## Files description
+ dockerfile : contains all initializations needed for our container (some are optional)
+ requirements.txt : contains some Python that should be installed
+ service.py : defining all services needed.
+ app.py : defining all web communications and the main of the app.
+ Templates : contains all templates (.html) needed
+ Static : contains all styles (.CSS) needed.

## Notes
+ The app should run as root.
+ 2 users are created initially. /home/user1 has a tree created in dockerfile for testing purposes
+ The searchbar takes either the name of the file or its extension ex. 'a1' or 'txt'or 'a1.txt'.
