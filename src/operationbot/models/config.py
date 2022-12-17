"""Pydantic Settings version of secret.py and config.py"""


from typing import Literal

from pydantic import BaseSettings


class Secret(BaseSettings):
    """A secret.py file contents"""

    version: Literal["1"]
    token: str
    command_char: str
    admins: list[int]
    admin: int
    debug: bool = False
    signoff_notify_user: int
    platoon_size: str
    ww2_mods: str

    class Config:
        """The config for the secret object"""

        env_prefix = "OPBOT_"


# TODO Move "src/operationbot/config.py" here too
#
# class SiteConfig(BaseSettings):
#     """Configuration that is unique to this deployment 'site'"""

#     version: Literal[12]
#     json_filepaths: dict[str, str] = {"events":  "database/events.json",
#                                       "archive": "database/archive.json"}
#     additional_role_emojis: list[str] = [
#         "\N{DIGIT ONE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
#         "\N{DIGIT TWO}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
#         "\N{DIGIT THREE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
#         "\N{DIGIT FOUR}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
#         "\N{DIGIT FIVE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
#         "\N{DIGIT SIX}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
#         "\N{DIGIT SEVEN}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
#         "\N{DIGIT EIGHT}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
#         "\N{DIGIT NINE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
#         "\N{KEYCAP TEN}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
#         "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
#         ]
