from datetime import datetime

import pytest

from eventDatabase import EventDatabase


@pytest.fixture(name="database")
def fixturedatabase():
    # This makes sure that the database is cleared between each test
    EventDatabase.events = {}
    EventDatabase.nextID = 0
    EventDatabase.offline_load = True
    return EventDatabase


def test_main_event(database: EventDatabase):
    date = datetime(2020, 1, 1, 12, 0)
    event = database.createEvent(date)
    assert event.date == date


def test_sideop(database: EventDatabase):
    date = datetime(2020, 1, 1, 12, 0)
    event = database.createEvent(date, sideop=True)
    assert event.sideop


def test_platoon_size(database: EventDatabase):
    date = datetime(2020, 1, 1, 12, 0)
    event = database.createEvent(date, platoon_size='1PLT')
    assert event.platoon_size == '1PLT'


# def test_event_text():
#     database = EventDatabase
#     database.loadDatabase(offline_load=True)
#     event = database.events[766]
#     assert event.text == "The first side operation in the game.\n\n"
