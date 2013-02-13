import re
from collections import OrderedDict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pelican import signals
from pelican.utils import get_date

def month_range(start_date, end_date):
    """Given a start date and end date, yield a sequence of start-of-month datetimes"""
    date = start_date.replace(day=1,hour=0,minute=0,second=0,microsecond=0)

    while date.year < end_date.year or (date.year == end_date.year and date.month <= end_date.month):
        yield date
        date += relativedelta(months=+1)

def events_by_month(events):
    """Given a list of events, yields a sequence of (month_name, [events]) tuples"""

    for month in month_range(events[0].date, events[-1].date):
        yield (month.strftime("%B"), [ev for ev in events if ev.date.month == month.month and ev.date.year == month.year])

def generate_calendar(generator):
    now = datetime.now()
    events = [article for article in generator.articles if article.date >= now and article.category == 'events']
    events.reverse()

    calendar = OrderedDict()

    featured_event = None
    for month, events in events_by_month(events):
        calendar[month] = events
        for event in events:
            event.end_date = get_date(event.end_date)

            if not featured_event and event.metadata.has_key('featured'):
                featured_event = event

    generator.calendar = calendar
    generator.featured_event = featured_event or calendar.values()[0][0]
    generator._update_context(('calendar','featured_event'))

def register():
    signals.article_generator_finalized.connect(generate_calendar)


def emailize(text):
    return re.sub('([a-zA-Z.+-]+@[a-zA-Z.+-]+)', '<a href="mailto:\\1">\\1</a><br/>', text)
