"""Pydantic compatible models"""


from pydantic import BaseModel, Field


class RootEvent(BaseModel):
    """An event in JSON"""

    next_id: int = Field(alias="nextID")

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
