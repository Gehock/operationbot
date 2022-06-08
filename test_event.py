from datetime import datetime, time

from config import EMBED_COLOR
from event import Event


def test_default():
    date = datetime(2020, 1, 1, 12, 0, 0)
    event = Event(date, (), platoon_size='empty')

    assert event.date == date
    assert event.time == time(hour=date.hour, minute=date.minute)
    date = datetime(2020, 1, 2, 12, 0, 0)
    event.date = date
    assert event.date == date

    event.faction = 'USMC'
    assert event.faction == 'USMC'

    event.terrain = 'Stratis'
    assert event.terrain == 'Stratis'

    assert event.title == 'Operation'
    assert event.description == ''
    assert event.createEmbed().description == (
        f"Local time: <t:{int(date.timestamp())}> "
        f"(<t:{int(date.timestamp())}:R>)"
        f"\nTerrain: Stratis - Faction: USMC")


def test_dlc():
    date = datetime(2020, 1, 1, 12, 0, 0)
    event = Event(date, (), platoon_size='empty')

    event.terrain = 'Tanoa'
    assert event.terrain == 'Tanoa'
    assert event.faction == 'unknown'
    assert event.title == 'APEX Operation'
    assert event.description == ''
    assert event.createEmbed().description == (
        f"Local time: <t:{int(date.timestamp())}> "
        f"(<t:{int(date.timestamp())}:R>)"
        f"\nTerrain: {event.terrain} - Faction: {event.faction}\n\n"
        f"The **{event.dlc} DLC** is required to join this event")
    event.terrain = 'Stratis'
    assert event.dlc is None
    event.dlc = 'GlobMob'
    assert event.dlc == 'GlobMob'


def test_ww2():
    date = datetime(2020, 1, 1, 12, 0)
    event = Event(date, (), platoon_size='WW2side', sideop=True)
    assert event.title == "WW2 Side Operation"


def test_colours():
    date = datetime(2020, 1, 1, 12, 0)
    event = Event(date, (), platoon_size='empty')
    assert event.color == EMBED_COLOR['DEFAULT']

    event = Event(date, (), platoon_size='empty', sideop=True)
    assert event.color == EMBED_COLOR['SIDEOP']

    event = Event(date, (), platoon_size='WW2side', sideop=True)
    assert event.color == EMBED_COLOR['WW2']

    event = Event(date, (), platoon_size='empty')
    event.terrain = 'Livonia'
    assert event.color == EMBED_COLOR['DLC']

    event = Event(date, (), platoon_size='empty', sideop=True)
    event.terrain = 'Livonia'
    assert event.color == EMBED_COLOR['DLC_SIDEOP']
