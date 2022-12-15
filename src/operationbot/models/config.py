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
