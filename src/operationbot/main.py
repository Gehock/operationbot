#!/usr/bin/env python3
import logging
import sys

import discord

from operationbot import config as cfg
from operationbot.bot import OperationBot
from operationbot.models.config import Secret

CONFIG_VERSION = 12
if cfg.VERSION != CONFIG_VERSION:
    raise ValueError(
        f"Incompatible config file, expecting version {CONFIG_VERSION}, "
        f"found version {cfg.VERSION}"
    )

initial_extensions = [
    "operationbot.commandListener",
    "operationbot.eventListener",
    "operationbot.cogs.repl",
]


if sys.version_info < (3, 10):
    raise Exception("Must be run with Python 3.10 or higher")


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("discord").setLevel(logging.INFO)
    logging.getLogger("discord.gateway").setLevel(logging.WARNING)
    logging.info("Loading config and secrets")
    s = Secret()  # Or via yaml.safe_load

    intents = discord.Intents.default()
    intents.members = True  # pylint: disable=assigning-non-slot
    intents.messages = True  # pylint: disable=assigning-non-slot
    bot = OperationBot(secrets=s, command_prefix=s.COMMAND_CHAR, intents=intents)
    # bot.remove_command("help")

    print("Starting up")
    bot.load_extension("operationbot.reload")
    print("Loading extensions")
    for extension in initial_extensions:
        # try:
        bot.load_extension(extension)
        # except Exception:
        #     print(f'failed to load extension {extension}')
    print("Running")
    bot.run(s.TOKEN)
