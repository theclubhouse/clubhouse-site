#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import pelcalendar

AUTHOR = u"theClubhou.se"
SITENAME = u"theClubhou.se"
SITEURL = 'http://theclubhou.se'

TIMEZONE = 'America/New_York'
THEME = 'themes/theclubhouse'
JINJA_EXTENSIONS = ['jinja2.ext.with_']
JINJA_FILTERS = {'emailify': pelcalendar.emailize}

DEFAULT_LANG = 'en'

PATH='content'
USE_FOLDER_AS_CATEGORY=True
NEWEST_FIRST_ARCHIVES=False

# Blogroll
LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pcooo.org'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}.html'

PLUGIN_PATH=''
PLUGINS=['pelcalendar']
