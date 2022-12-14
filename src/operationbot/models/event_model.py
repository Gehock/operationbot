"""Pydantic compatible models"""

from datetime import date, time
from typing import Literal, Optional

from pydantic import BaseModel, Field

DiscordID = int
"""An ID in discord, regardless of what it points to (Msg or Chan)"""


class Role(BaseModel):
    """A single role (to sign up to)"""

    name: str
    emoji: Optional[str] = None
    show_name: bool
    user_id: Optional[DiscordID] = Field(alias="userID")
    user_name: str = Field(alias="userName")


class RoleGroup(BaseModel):
    """A grouping of roles, each role is signup-able"""

    name: str
    is_inline: bool = Field(alias="isInline")
    # roles: list[Role]   # Ideally this, but actually:
    roles: dict[str, Role]


RoleGroups = dict[str, RoleGroup]
"""Lookup table for RoleGroup, by name"""


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
    message_id: DiscordID = Field(
        alias="messageID", description="The Discord Message ID"
    )
    platoon_size: Literal["1PLT"]
    sideop: bool
    attendees: dict  # TODO Get specific
    role_groups: RoleGroups = Field(alias="roleGroups")
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
    #     self.roleGroups: = {}
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
