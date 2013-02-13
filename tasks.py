#!/usr/bin/env python

import re, codecs
import datetime
import dateutil.rrule
from dateutil.rrule import *
from icalendar import Calendar
import pytz
from jinja2.utils import urlize

Translations = {
    'MAX CLASS SIZE': 'Class_Size',
    'COST TO PUBLIC': 'Cost',
    'COST': 'Cost',
    'COST TO MEMBERS': 'Cost_Member',
    'CLASS COST (PUBLIC)': 'Cost',
    'CLASS COST (MEMBERS)': 'Cost_Member',
    'SIGN-UP LINK': 'RSVP_Link',
    'TEACHER': 'Teacher',
    'TO SIGN-UP FOR THE CLASS': 'RSVP_Email',
    'TO SIGN-UP': 'RSVP_Email',
    'FEATURED': 'Featured'
}

def read_calendar(filename):
    with file(filename, 'rb') as f:
        return Calendar.from_ical(f.read())


def format_description(body):
    """Converts a GCal description to Markdown"""
    output = re.sub('^\n+', '', body, flags=re.MULTILINE)
    output = re.sub('\n+', '\n\n', output, flags=re.MULTILINE)
    output = re.sub('^-', '* ', output, flags=re.MULTILINE)
    output = re.sub('([A-Z \t]+):\s+$', '#### \\1', output, flags=re.MULTILINE)
    return output

def parse_description(body):
    output = ''
    metadata = {}

    for line in body.splitlines():
#        line = re.sub('([a-zA-Z.+-]+@[a-zA-Z.+-]+).?', '<a href="mailto:\\1">\\1</a><br/>', line)
#        line = re.sub('([a-zA-Z.+-]+@[a-zA-Z.+-]+).?', 'mailto:\\1<br/>', line)
        match = re.match('([^:]+): (.*)', line)
        key, value = match and match.groups() or (None, None)

        if key and key.upper() in Translations.keys():
            metadata[Translations[key.upper()]] = value
        else:
#            if "<" not in line and ">" not in line:
#            line = urlize(line, trim_url_limit=32)
            #line = re.sub('(http(s?):[^ ]+)', '<a href="\\1">\\1</a>', line)
            output += line + "\n"

    return format_description(output), metadata


def normalize_date(date, tzinfo=None):
    if type(date) is datetime.date:   # icalendar returns datetime.date for all-day events
        date = datetime.datetime.combine(date, datetime.time())
        return date.replace(tzinfo=tz)
    return date.astimezone(tzinfo)

if __name__ == '__main__':
    gcal = read_calendar('./clubhouse.ics')
    events = [e for e in gcal.walk() if e.name == 'VEVENT']
    tz = pytz.timezone('America/New_York')

    for e in events:
        title = e['summary']
        date = normalize_date(e['dtstart'].dt, tzinfo=tz)
        date = date.astimezone(tz)
        dates = [date]

        if e.has_key('RRULE'):
            rr = e['RRULE']
            if len(rr['freq']) > 1:
                print "Got more than one recurrence rule for %s, skipping" % (title,)
            else:
#                import pdb; pdb.set_trace()
                if rr['byday'] and len(rr['byday'][0]) > 2:
                    weird_rrule_day = rr['byday'][0][-2:]
                    weird_rrule_modifier = int(rr['byday'][0][0:-2])
                    dates = list(rrule(getattr(dateutil.rrule, rr['freq'][0]),
                                       byweekday=getattr(dateutil.rrule, weird_rrule_day)(weird_rrule_modifier),
                                       dtstart=date,
                                       count=(rr.has_key('count') and rr['COUNT'][0] or 5)))

                else:
                    dates = list(rrule(getattr(dateutil.rrule, rr['freq'][0]),
                                       byweekday=getattr(dateutil.rrule, rr['byday'][0]),
                                       dtstart=date,
                                       count=(rr.has_key('count') and rr['COUNT'][0] or None)))



        for date in dates:
            filename = date.strftime('%F_') + re.sub('[^a-zA-Z_]', '', title.replace(' ', '_'))

            with codecs.open(u'content/events/%s.md' % filename, 'w', encoding='utf-8') as f:
                print >>f, 'Title: ' + e['summary']
                print >>f, 'Date: ' + date.strftime("%F %T")
                print >>f, 'End_Date: ' + normalize_date(e['dtend'].dt, tzinfo=tz).strftime("%F %T")

                body, metadata = parse_description(e['description'])

                for key, value in metadata.items():
                    print >>f, '%s: %s' % (key, value)

                print >>f, ''
                print >>f, body


