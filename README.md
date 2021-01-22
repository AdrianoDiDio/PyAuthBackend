# PyAuthBackend

Table of contents
=================

   * [PyAuthBackend](#PyAuthBackend)
   * [Table of contents](#table-of-contents)
   * [Requirements](#requirements)
   * [Installation](#installation)
   * [Usage](#usage)
      * [STDIN](#stdin)
      * [Local files](#local-files)
      * [Remote files](#remote-files)
      * [Multiple files](#multiple-files)
      * [Combo](#combo)
      * [Auto insert and update TOC](#auto-insert-and-update-toc)
      * [GitHub token](#github-token)
      * [TOC generation with Github Actions](#toc-generation-with-github-actions)
   * [Tests](#tests)
   * [Dependency](#dependency)
   * [Docker](#docker)
     * [Local](#local)
     * [Public](#public)

Requirements
============
This guide assumes that a Linux distribution is used, commands for Windows are similar but requires some steps to get the required files.
In order to setup this package we need to install python3,pip,mysql using a simple bash command (Note that sudo may be required in order to install it):
```bash
$ apt-install python3,pip,mysql-server
```
After installing the required packages the installation can proceed.

Installation
============
After unzipping the package, we need to create a new virtual enviroment.
Virtual Enviroment let us create a separate enviroment from the system to install local dependencies required by this package.
In order to create a new enviroment, open up the shell in the folder where the project was unzipped and run:
```bash
$ python3 -m venv env
```
This will create an hidden folder called .env that will contains all the required files to run the project.
Next, we need to activate it by running:
```bash
$ source .env/bin/activate
```
Now, we need to download all the required files by running:
```bash
$ pip install -r requirements.txt
```
After pip is done installing, we need to setup our database using django utilities.  
Before running the commands, modify the section DATABASES inside the file PyAuthBackend/settings.py by inserting the MySQL  
Username,Password,DBName and Host.  
If any of the parameters is wrong or missing DJango will display an error asking to fix it.  
Next, we need to prepare our query needed to create the Database structure by running the command:
```bash
$ python manage.py makemigrations
```
and then:
```bash
$ python manage.py migrate
```
If all the commands completed without error, we can now start the local development server by running:
```bash
$ python manage.py runserver <OptionalIPAddress:Port>
```
If IP address is not specified, server will be available at localhost:8000.
