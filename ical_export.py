from icalendar import Calendar as iCalendar
from icalendar import Event as iEvent

from event import Event as ZeusEvent


def to_ical(zevent: ZeusEvent) -> iEvent:
    """Converts a Zeus event to an ical Event (sub)object"""
    ievent = iEvent()
    ievent['uid'] = zevent.id
    ievent['summary'] = zevent.title  # FIXME: Moar words
    ievent['dtstart'] = zevent.date
    return ievent


def generate_calendar(ical_events: list[iEvent]) -> iCalendar:
    """Aggregates given ical events into a calendar object"""
    calendar = iCalendar()
    for ical_event in ical_events:
        calendar.add_component(ical_event)
    return calendar


def create_ical_file(ical: iCalendar, filepath: str):
    with open(filepath, 'wb') as ical_file:
        ical_file.write(ical.to_ical())
        # ical_file.write(b"\n")  # End of file newline


if __name__ == '__main__':
    # Fetch a few zeus events, left up to the reader:
    # zevents: list[ZeusEvent] = magic_event_fetcher()
    zevents = []  # type: ignore
    ievents = [to_ical(zevent) for zevent in zevents]
    cal = generate_calendar(ievents)
    create_ical_file(cal, "zeus_events.ics")
