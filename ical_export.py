from datetime import timedelta
from zoneinfo import ZoneInfo

# import logging
from ics import Calendar, Event

from event import Event as ZeusEvent
from eventDatabase import EventDatabase


def to_ical(operation: ZeusEvent) -> Event:
    """Converts a Zeus operation to an ical Event (sub)object"""
    event = Event()
    event.uid = f"zeusops-operation-{operation.id}"
    date = operation.date.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
    event.name = operation.title  # FIXME: Moar words
    event.begin = date
    event.end = date + timedelta(hours=2, minutes=30)
    event.created = date
    event.description = operation.text
    return event


def generate_calendar(ical_events: list[Event]) -> Calendar:
    """Aggregates given ical events into a calendar object"""
    cal = Calendar()
    # cal.add('prodid', '-//Zeusops//Operation calendar//EN')
    # cal.add('version', '2.0')
    for event in ical_events:
        cal.events.add(event)
    return cal


if __name__ == '__main__':
    EventDatabase.loadDatabase(offline_load=True)

    events = [to_ical(event) for event in EventDatabase.events.values()]
    calendar = generate_calendar(events)
    with open("zeus_events.ics", 'w') as f:
        f.write(str(calendar))
