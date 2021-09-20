import discord
from discord.ext.commands import Context

def is_dm(ctx: Context):
    return not isinstance(ctx.channel, discord.abc.GuildChannel)
