"""Pydantic compatible models"""

from datetime import date, time
from typing import Literal, Optional

from pydantic import BaseModel, Field

DiscordID = int
"""An ID in discord, regardless of what it points to (Msg or Chan)"""


class Event(BaseModel):
    """A single event"""

    title: Optional[str]
    date: date
    description: str
    """A cool description for our op"""
    time: time
    terrain: str
    faction: str
    port: int
    mods: str
    message_id: DiscordID = Field(alias="messageID")
    platoon_size: Literal["1PLT"]
    sideop: bool
    attendees: dict  # TODO Get specific
    role_groups: dict = Field(alias="roleGroups")
    dlc: Optional[str] = None

    # def __init__(self, date: datetime.datetime, guildEmojis: Tuple[Emoji, ...],
    #              eventID=0, importing=False, sideop=False, platoon_size=None):
    #     self._title: Optional[str] = None
    #     self.date = date
    #     self._terrain = TERRAIN
    #     self.faction = FACTION
    #     self.description = DESCRIPTION
    #     self.port = cfg.PORT_DEFAULT
    #     self.mods = MODS
    #     self.roleGroups: Dict[str, RoleGroup] = {}
    #     self.messageID = 0
    #     self.id = eventID
    #     self.sideop = sideop
    #     self.attendees: list[Union[User, discord.abc.User]] = []
    #     self.dlc: Optional[str] = None


EventID = int
"""An Event's unique ID"""

EventMap = dict[EventID, Event]
"""A map of  Events indexed by their EventID"""


class RootEvent(BaseModel):
    """The JSON root for Event saving"""

    version: Literal[4]
    next_id: int = Field(alias="nextID")
    events: EventMap
