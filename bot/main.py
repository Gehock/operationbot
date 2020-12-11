#!/usr/bin/env python3
from bot import config as cfg
from bot.operationbot import OperationBot
from bot.secret import COMMAND_CHAR, TOKEN

CONFIG_VERSION = 8
if cfg.VERSION != CONFIG_VERSION:
    raise Exception(
        "Incompatible config file, expecting version {}, found version {}"
        .format(CONFIG_VERSION, cfg.VERSION))

initial_extensions = ['bot.commandListener',
    'bot.eventListener', 'bot.cogs.repl']
bot = OperationBot(command_prefix=COMMAND_CHAR)
# bot.remove_command("help")

if __name__ == '__main__':
    print("Starting up")
    bot.load_extension('bot.reload')
    print("Loading extensions")
    for extension in initial_extensions:
        # try:
        bot.load_extension(extension)
        # except Exception:
        #     print(f'failed to load extension {extension}')
    print("Running")
    bot.run(TOKEN)
