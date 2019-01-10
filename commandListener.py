import importlib
import sys
import traceback
from datetime import datetime

from discord import NotFound, Message
from discord.ext.commands import (BadArgument, Bot, Context, Converter,
                                  MissingRequiredArgument, command)

import config as cfg
from main import eventDatabase
from secret import COMMAND_CHAR as CMD


class EventDate(Converter):
    async def convert(self, ctx: Context, arg: str) -> datetime:
        try:
            date = datetime.strptime(arg, '%Y-%m-%d')
        except ValueError:
            raise BadArgument("Invalid date format")
        return date.replace(hour=18, minute=45)


class EventTime(Converter):
    async def convert(self, ctx: Context, arg: str) -> datetime:
        try:
            time = datetime.strptime(arg, '%H:%M')
        except ValueError:
            raise BadArgument("Invalid time format")
        return time


class EventMessage(Converter):
    async def convert(self, ctx: Context, arg: str) -> Message:
        try:
            messageid = int(arg)
        except ValueError:
            raise BadArgument("Invalid message ID, needs to be an "
                              "integer")

        # Get channels
        eventchannel = ctx.bot.get_channel(cfg.EVENT_CHANNEL)

        # Get message
        try:
            return await eventchannel.get_message(messageid)
        except NotFound:
            raise BadArgument("No message found with that message ID")


class CommandListener:

    def __init__(self, bot: Bot):
        self.bot = bot
        self.eventDatabase = eventDatabase

    @command(
        help="Execute arbitrary code\n"
             "Example: {}exec print(\"Hello World\")".format(CMD))
    async def exec(self, ctx: Context, *, cmd: str):
        # Allow only Gehock#9738 to send commands for security
        if ctx.message.author.id != 150625032656125952:
            await ctx.send("Unauthorized")
            return

        try:
            msg = eval(cmd)
        except Exception:
            msg = "An error occured while executing: ```{}```" \
                  .format(traceback.format_exc())
        await ctx.send(msg)

    # Create event command
    @command(
        help="Create a new event\n"
             "Example: {}create 2019-01-01".format(CMD))
    async def create(self, ctx: Context, date: EventDate):
        eventchannel = self.bot.get_channel(cfg.EVENT_CHANNEL)

        # Create event and sort events, export
        msg, event = await self.eventDatabase.createEvent(date, eventchannel)
        await self.eventDatabase.updateReactions(msg, event, self.bot)
        await self.sortEvents(ctx)
        self.writeJson()  # Update JSON file
        await ctx.send("Created event: {}".format(event))

    # Add additional role to event command
    @command(
        help="Add a new additional role to the event\n"
             "Example: {}addrole 530481556083441684 Y1 (Bradley) Driver"
             .format(CMD))
    async def addrole(self, ctx: Context, eventMessage: EventMessage, *,
                      rolename: str):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        reaction = eventToUpdate.addAdditionalRole(rolename)
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        await self.eventDatabase.addReaction(eventMessage, reaction)
        self.writeJson()  # Update JSON file
        await ctx.send("Role added")

    # Remove additional role from event command
    @command(
        help="Remove an additional role from the event\n"
             "Example: {}removerole 530481556083441684 Y1 (Bradley) Driver"
             .format(CMD))
    async def removerole(self, ctx: Context, eventMessage: EventMessage, *,
                         rolename: str):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # Find role
        role = eventToUpdate.findRoleWithName(rolename)
        if role is None:
            await ctx.send("No role found with that name")
            return

        # Remove reactions, remove role, update event, add reactions, export
        for reaction in eventToUpdate.getReactionsOfGroup("Additional"):
            await eventMessage.remove_reaction(reaction, self.bot.user)
        eventToUpdate.removeAdditionalRole(rolename)
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        for reaction in eventToUpdate.getReactionsOfGroup("Additional"):
            await self.eventDatabase.addReaction(eventMessage, reaction)
        self.writeJson()  # Update JSON file
        await ctx.send("Role removed")

    # Set title of event command
    @command(
        help="Set event title\n"
             "Example: {}settitle 530481556083441684 Operation Striker"
             .format(CMD))
    async def settitle(self, ctx: Context, eventMessage: EventMessage, *,
                       title: str):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # Change title, update event, export
        # NOTE: Does not check for too long input. Will result in an API error
        # and a bot crash
        eventToUpdate.setTitle(title)
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        self.writeJson()  # Update JSON file
        await ctx.send("Title set")

    # Set date of event command
    @command(
        help="Set event date\n"
             "Example: {}setdate 530481556083441684 2019-01-01"
             .format(CMD))
    async def setdate(self, ctx: Context, eventMessage: EventMessage,
                      date: EventDate):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # Change date
        eventToUpdate.setDate(date)

        # Update event and sort events, export
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        await self.sortEvents(ctx)
        self.writeJson()  # Update JSON file
        await ctx.send("Date set")

    # Set time of event command
    @command(
        help="Set event time\n"
             "Example: {}settime 530481556083441684 18:45"
             .format(CMD))
    async def settime(self, ctx: Context, eventMessage: EventMessage,
                      time: EventTime):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # Change time
        eventToUpdate.setTime(time)

        # Update event and sort events, export
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        await self.sortEvents(ctx)
        self.writeJson()  # Update JSON file
        await ctx.send("Time set")

    # Set terrain of event command
    @command(
        help="Set event terrain\n"
             "Example: {}settime 530481556083441684 Takistan"
             .format(CMD))
    async def setterrain(self, ctx: Context, eventMessage: EventMessage, *,
                         terrain: str):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # Change terrain, update event, export
        eventToUpdate.setTerrain(terrain)
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        self.writeJson()  # Update JSON file
        await ctx.send("Terrain set")

    # Set faction of event command
    @command(
        help="Set event faction\n"
             "Example: {}setfaction 530481556083441684 Insurgents"
             .format(CMD))
    async def setfaction(self, ctx: Context, eventMessage: EventMessage, *,
                         faction: str):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # Change faction, update event, export
        eventToUpdate.setFaction(faction)
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        self.writeJson()  # Update JSON file
        await ctx.send("Faction set")

    # Set faction of event command
    @command(
        help="Set event description\n"
             "Example: {}setdescription 530481556083441684 Insurgents"
             .format(CMD))
    async def setdescription(self, ctx: Context, eventMessage: EventMessage, *,
                         description: str):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # Change description, update event, export
        eventToUpdate.description = description
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        self.writeJson()  # Update JSON file
        await ctx.send("Description set")

    # Sign user up to event command
    @command(
        help="Sign user up (manually)\n"
             "Example: {}signup 530481556083441684 165853537945780224 "
             "Y1 (Bradley) Gunner"
             .format(CMD))
    async def signup(self, ctx: Context, eventMessage: EventMessage,
                     userid: int, *, roleName: str):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # TODO: Replace with Member Converter
        user = ctx.guild.get_member(userid)
        if user is None:
            await ctx.send("No user found with that user ID")
            return

        # Find role
        role = eventToUpdate.findRoleWithName(roleName)
        if role is None:
            await ctx.send("No role found with that name")
            return

        # Sign user up, update event, export
        eventToUpdate.signup(role, user)
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        self.writeJson()  # Update JSON file
        await ctx.send("User signed up")

    # Remove signup on event of user command
    @command(
        help="Undo user signup (manually)\n"
             "Example: {}removesignup 530481556083441684 165853537945780224 "
             "Y1 (Bradley) Gunner"
             .format(CMD))
    async def removesignup(self, ctx: Context, eventMessage: EventMessage,
                           userid: int, *, roleName: str):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # TODO: Replace with Member Converter
        user = self.bot.get_user(userid)
        if user is None:
            await ctx.send("No user found with that user ID")
            return

        # Remove signup, update event, export
        eventToUpdate.undoSignup(user)
        await self.eventDatabase.updateEvent(eventMessage, eventToUpdate)
        self.writeJson()  # Update JSON file
        await ctx.send("User signup removed")

    # Archive event command
    @command(
        help="Archive event\n"
             "Example: {}archive 530481556083441684"
             .format(CMD))
    async def archive(self, ctx: Context, eventMessage: EventMessage):
        eventToUpdate = await self.getEvent(eventMessage.id, ctx)
        if eventToUpdate is None:
            return

        # eventchannel = self.bot.get_channel(cfg.EVENT_CHANNEL)
        eventarchivechannel = self.bot.get_channel(cfg.EVENT_ARCHIVE_CHANNEL)

        # Archive event and export
        await self.eventDatabase.archiveEvent(eventMessage, eventToUpdate,
                                              eventarchivechannel)
        self.writeJson()  # Update JSON file
        await ctx.send("Event archived")

    # Delete event command
    @command(
        help="Delete event\n"
             "Example: {}delete 530481556083441684"
             .format(CMD))
    async def delete(self, ctx: Context, eventMessage: EventMessage):
        # Get info from context
        info = ctx.message.content
        info = info.split(" ")
        if len(info) != 2:
            await ctx.send("Usage: delete MESSAGEID")
            return

        # Get message ID
        eventMessageID = eventMessage.id

        # Delete event
        event = self.eventDatabase.findEvent(eventMessageID)
        if event is not None:
            eventchannel = ctx.bot.get_channel(cfg.EVENT_CHANNEL)
            try:
                eventMessage = await eventchannel.get_message(eventMessageID)
            except NotFound:
                await ctx.send("No message found with that message ID")
                return
            await self.eventDatabase.removeEvent(eventMessage)
            await ctx.send("Removed event from events")
        else:
            event = self.eventDatabase.findEventInArchive(eventMessageID)
            if event is not None:
                eventMessage = await self.getMessageFromArchive(eventMessageID,
                                                                ctx)
                await self.eventDatabase.removeEventFromArchive(eventMessage)
                await ctx.send("Removed event from events archive")
            else:
                await ctx.send("No event found with that message ID")

        self.writeJson()  # Update JSON file

    # sort events command
    @command(help="Sort events (manually)")
    async def sort(self, ctx: Context):
        await self.sortEvents(ctx)
        await ctx.send("Events sorted")

    # export to json
    @command(help="Export eventDatabase (manually)")
    async def export(self, ctx: Context):
        self.writeJson()
        await ctx.send("EventDatabase exported")

    # import from json
    @command(name="import", help="Export eventDatabase (manually)")
    async def importJson(self, ctx: Context):
        await self.readJson()
        await ctx.send("EventDatabase imported")

    @command(help="Shut down the bot")
    async def shutdown(self, ctx: Context):
        await ctx.send("Shutting down")
        print("logging out")
        await self.bot.logout()
        print("exiting")
        sys.exit()

    # TODO: Test commands
    @exec.error
    @create.error
    @addrole.error
    @removerole.error
    @settitle.error
    @settime.error
    @setterrain.error
    @setfaction.error
    @signup.error
    @removesignup.error
    @archive.error
    @delete.error
    @importJson.error
    @export.error
    async def command_error(self, ctx: Context, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Missing argument. See: {}help {}"
                           .format(CMD, ctx.command))
        elif isinstance(error, BadArgument):
            await ctx.send("Invalid argument: {}. See: {}help {}"
                           .format(error, CMD, ctx.command))
        else:
            await ctx.send("Unexpected error occured:", error.message)
            print(error)

    # Returns message from archive from given string or gives an error
    async def getMessageFromArchive(self, messageID: int, ctx: Context):
        # Get messageID

        # Get channels
        eventarchivechannel = ctx.bot.get_channel(cfg.EVENT_ARCHIVE_CHANNEL)

        # Get message
        try:
            return await eventarchivechannel.get_message(messageID)
        except Exception:
            await ctx.send("No message found in archive with that message ID")
            return

    async def getEvent(self, messageID, ctx: Context):
        eventToUpdate = self.eventDatabase.findEvent(messageID)
        if eventToUpdate is None:
            await ctx.send("No event found with that message ID")
            return None
        return eventToUpdate

    # Sort events in eventDatabase
    async def sortEvents(self, ctx: Context):
        self.eventDatabase.sortEvents()

        for messageID, event_ in self.eventDatabase.events.items():
            eventchannel = ctx.bot.get_channel(cfg.EVENT_CHANNEL)
            try:
                eventMessage = await eventchannel.get_message(messageID)
            except NotFound:
                await ctx.send("No message found with that message ID")
                return
            await self.eventDatabase.updateReactions(eventMessage, event_,
                                                     self.bot)
            await self.eventDatabase.updateEvent(eventMessage, event_)

    # Export eventDatabase to json
    def writeJson(self):
        self.eventDatabase.toJson()

    # Clear eventchannel and import eventDatabase from json
    async def readJson(self):
        await self.eventDatabase.fromJson(self.bot)


def setup(bot):
    # importlib.reload(event)
    importlib.reload(cfg)
    bot.add_cog(CommandListener(bot))
