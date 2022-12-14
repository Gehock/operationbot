"""Checking that we can import existing events via Pydantic"""

import json

from operationbot.models.event_model import RootEvent


def test_import_simple(shared_datadir):
    """Import the current events (small batch)"""
    event_str = (shared_datadir / "events.json").read_text()
    event_dict = json.loads(event_str)
    event = RootEvent.parse_obj(event_dict)
    assert event.next_id == 858, "Bad parsed object"
