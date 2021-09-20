from datetime import datetime
from typing import Tuple

from discord.embeds import Embed
from discord.emoji import Emoji

import config as cfg
from event import Event

DRAFT_PREFIX = "[Draft]"


class EventDraft(Event):
    def __init__(self, date: datetime, guildEmojis: Tuple[Emoji], eventID=0,
                 importing=False, sideop=False, platoon_size=None,
                 manager_role_name=None):
        super().__init__(date, guildEmojis, eventID=eventID, importing=importing, sideop=sideop, platoon_size=platoon_size)
        self.title = f"{DRAFT_PREFIX} {self.title}"
        self.manager_role_name = manager_role_name

    def createEmbed(self) -> Embed:
        embed = super().createEmbed()
        footer = (f"{embed.footer.text}\n"
                  f"Users with role '{self.manager_role_name}' can manage "
                  f"this draft with reactions:\n"
                  f"{cfg.DRAFT_DELETE}: delete, "
                  f"{cfg.DRAFT_PUBLISH}: publish, {cfg.DRAFT_EDIT}: edit")
        embed.set_footer(text=footer)
        return embed
