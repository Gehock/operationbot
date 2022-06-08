from datetime import datetime, time
from typing import Union

import pytest
from discord import Emoji

from config import EMBED_COLOR
from event import Event


def test_default():
    date = datetime(2020, 1, 1, 12, 0, 0)
    event = Event(date, offline_load=True)

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
    event = Event(date, offline_load=True)

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


def test_sideop():
    date = datetime(2020, 1, 1, 12, 0)
    event = Event(date, offline_load=True, sideop=True)
    assert event.sideop


def test_1plt():
    date = datetime(2020, 1, 1, 12, 0)
    event = Event(date, offline_load=True, platoon_size='1PLT')
    assert event.platoon_size == '1PLT'


def test_unknown_size():
    date = datetime(2020, 1, 1, 12, 0)
    with pytest.raises(ValueError):
        Event(date, offline_load=True, platoon_size='unknown')


def test_ww2():
    date = datetime(2020, 1, 1, 12, 0)
    event = Event(date, offline_load=True, platoon_size='WW2side', sideop=True)
    assert event.title == "WW2 Side Operation"


def test_colours():
    date = datetime(2020, 1, 1, 12, 0)
    event = Event(date, offline_load=True)
    assert event.color == EMBED_COLOR['DEFAULT']

    event = Event(date, offline_load=True, sideop=True)
    assert event.color == EMBED_COLOR['SIDEOP']

    event = Event(date, offline_load=True, platoon_size='WW2side', sideop=True)
    assert event.color == EMBED_COLOR['WW2']

    event = Event(date, offline_load=True)
    event.terrain = 'Livonia'
    assert event.color == EMBED_COLOR['DLC']

    event = Event(date, offline_load=True, sideop=True)
    event.terrain = 'Livonia'
    assert event.color == EMBED_COLOR['DLC_SIDEOP']


def _reaction_names(reactions: list[Union[str, Emoji]]) -> list[str]:
    # Reactions are either discord Emojis or unicode characters. For Emojis,
    # Emoji.name is used, unicode characters are used as is.
    return [
        reaction.name if isinstance(reaction, Emoji) else reaction
        for reaction in reactions
    ]


def test_reactions():
    date = datetime(2020, 1, 1, 12, 0)
    event = Event(date, offline_load=True, sideop=True)
    names = _reaction_names(event.getReactions())
    assert names == ["ASL", "A1", "A2", "\N{HEAVY PLUS SIGN}"]
