========================================
{{ project_name|title }} Django Project
========================================

Created by Klaus Laube - <klaube@gmail.com>


Prerequisites
==============

 - Python >=2.6
 - pip
 - virtualenv/virtualenvwrapper (optional)

=============
Installation
=============

Creating the environment
========================

Remove the wsgi.py::
    rm wsgi.py

Create a virtual python enviroment for the project. If you're not using virtualenv or virtualenvwrapper you may skip this step.

For virtualenvwrapper::

    mkvirtualenv --no-site-packages {{ project_name }}-env


For virtualenv::

    virtualenv --no-site-packages {{ project_name }}-env
    cd {{ project_name }}-env
    source bin/activate

===============
Clone the code
===============

Obtain the url to your git repository.::

    git clone <URL_TO_GIT_RESPOSITORY> {{ project_name }}

Install requirements
======================
::
    cd {{ project_name }}
    pip install -r requirements.txt
    Configure project

    cp {{ project_name }}/__local_settings.py {{ project_name }}/local_settings.py
    vi {{ project_name }}/local_settings.py

==============
Sync database
==============
::
    python manage.py syncdb

=========
Running
=========
::
    python manage.py runserver

Open browser to http://127.0.0.1:8000
