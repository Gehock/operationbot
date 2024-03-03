# import logging
from icalendar import Calendar as iCalendar
from icalendar import Event as iEvent

from event import Event as ZeusEvent
from eventDatabase import EventDatabase


def to_ical(zevent: ZeusEvent) -> iEvent:
    """Converts a Zeus event to an ical Event (sub)object"""
    ievent = iEvent()
    ievent['uid'] = zevent.id
    ievent['summary'] = zevent.title  # FIXME: Moar words
    ievent['dtstart'] = zevent.date
    return ievent


def generate_calendar(ical_events: list[iEvent]) -> iCalendar:
    """Aggregates given ical events into a calendar object"""
    cal = iCalendar()
    cal.add('prodid', '-//Zeusops//Operation calendar//EN')
    cal.add('version', '2.0')
    for ical_event in ical_events:
        cal.add_component(ical_event)
    return cal


def create_ical_file(ical: iCalendar, filepath: str):
    with open(filepath, 'wb') as ical_file:
        ical_file.write(ical.to_ical())
        # ical_file.write(b"\n")  # End of file newline


if __name__ == '__main__':
    # Fetch a few zeus events, left up to the reader:
    # zevents: list[ZeusEvent] = magic_event_fetcher()
    # logging.basicConfig(level=logging.WARNING)
    EventDatabase.loadDatabase(offline_load=True)
    ievents = [to_ical(zevent) for zevent in EventDatabase.events.values()]
    calendar = generate_calendar(ievents)
    create_ical_file(calendar, "zeus_events.ics")
