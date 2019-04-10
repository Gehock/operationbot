from datetime import datetime
from typing import Dict, Tuple, List

from discord import Embed, Emoji

import config as cfg
from role import Role
from roleGroup import RoleGroup

TITLE = "Operation"
TERRAIN = "unknown"
FACTION = "unknown"
DESCRIPTION = ""
COLOR = 0xFF4500


class Event:

    def __init__(self, date: datetime, guildEmojis: Tuple[Emoji],
                 importing=False):
        self.title = TITLE
        self.date = date
        self.terrain = TERRAIN
        self.faction = FACTION
        self.description = DESCRIPTION
        self.color = COLOR
        self.roleGroups: Dict[str, RoleGroup] = {}
        self.additionalRoleCount = 0

        self.normalEmojis = self.getNormalEmojis(guildEmojis)
        if not importing:
            self.addDefaultRoleGroups()
            self.addDefaultRoles()

    # Return an embed for the event
    def createEmbed(self) -> Embed:
        title = "{} ({})".format(
            self.title, self.date.strftime("%a %Y-%m-%d - %H:%M CET"))
        description = "Terrain: {} - Faction: {}\n\n{}".format(
            self.terrain, self.faction, self.description)
        eventEmbed = Embed(title=title, description=description,
                           colour=self.color)

        # Add field to embed for every rolegroup
        for group in self.roleGroups.values():
            if len(group.roles) > 0:
                eventEmbed.add_field(name=group.name, value=str(group),
                                     inline=group.isInline)

        return eventEmbed

    # Add default role groups
    def addDefaultRoleGroups(self):
        self.roleGroups["Company"] = RoleGroup("Company", isInline=False)
        self.roleGroups["Platoon"] = RoleGroup("Platoon")
        self.roleGroups["Alpha"] = RoleGroup("Alpha")
        self.roleGroups["Bravo"] = RoleGroup("Bravo")
        self.roleGroups["Additional"] = RoleGroup("Additional")

    # Add default roles
    def addDefaultRoles(self):
        for name, groupName in cfg.DEFAULT_ROLES.items():
            # Only add role if the group exists
            if groupName in self.roleGroups.keys():
                emoji = self.normalEmojis[name]
                newRole = Role(name, emoji, False)
                self.roleGroups[groupName].addRole(newRole)

    # Add an additional role to the event
    def addAdditionalRole(self, name: str) -> str:
        # Find next emoji for additional role
        emoji = cfg.ADDITIONAL_ROLE_EMOJIS[self.additionalRoleCount]

        # Create role
        newRole = Role(name, emoji, True)

        # Add role to additional roles
        self.roleGroups["Additional"].addRole(newRole)
        self.additionalRoleCount += 1

        return emoji

    def removeAdditionalRole(self, role: str):
        """Remove an additional role from the event."""
        # Remove role from additional roles
        self.roleGroups["Additional"].removeRole(role)

        # Reorder the emotes of all the additional roles
        self.additionalRoleCount = 0
        for roleInstance in self.roleGroups["Additional"].roles:
            emoji = cfg.ADDITIONAL_ROLE_EMOJIS[self.additionalRoleCount]
            roleInstance.emoji = emoji
            self.additionalRoleCount += 1

    def removeRoleGroup(self, groupName: str) -> bool:
        """
        Remove a role group.

        Returns false if the group cannot be found.
        """
        if groupName not in self.roleGroups:
            return False
        self.roleGroups.pop(groupName, None)
        return True

    # Title setter
    def setTitle(self, newTitle):
        self.title = newTitle

    # Date setter
    def setDate(self, newDate):
        self.date = self.date.replace(year=newDate.year, month=newDate.month,
                                      day=newDate.day)

    # Time setter
    def setTime(self, newTime):
        self.date = self.date.replace(hour=newTime.hour, minute=newTime.minute)

    # Terrain setter
    def setTerrain(self, newTerrain):
        self.terrain = newTerrain

    # Faction setter
    def setFaction(self, newFaction):
        self.faction = newFaction

    # Get emojis for normal roles
    def getNormalEmojis(self, guildEmojis):
        normalEmojis = {}

        for emoji in guildEmojis:
            if emoji.name in cfg.DEFAULT_ROLES:
                normalEmojis[emoji.name] = emoji

        return normalEmojis

    # Returns reactions of all roles
    def getReactions(self):
        reactions = []

        for roleGroup in self.roleGroups.values():
            role: Role
            for role in roleGroup.roles:
                emoji = role.emoji
                # Skip the ZEUS reaction. Zeuses can only be signed up using
                # the signup command
                if not (isinstance(emoji, Emoji) and emoji.name == "ZEUS"):
                    reactions.append(role.emoji)

        return reactions

    def getReactionsOfGroup(self, groupName: str) -> List[Emoji]:
        """Find reactions of a given role group."""
        reactions = []

        if groupName in self.roleGroups:
            for role in self.roleGroups[groupName].roles:
                reactions.append(role.emoji)

        return reactions

    def findRoleWithEmoji(self, emoji) -> Role:
        """Find a role with given emoji."""
        for roleGroup in self.roleGroups.values():
            for role in roleGroup.roles:
                if role.emoji == emoji:
                    return role
        return None

    def findRoleWithName(self, roleName: str) -> Role:
        """Find a role with given name."""
        roleName = roleName.lower()
        for roleGroup in self.roleGroups.values():
            role: Role
            for role in roleGroup.roles:
                if role.name.lower() == roleName:
                    return role
        return None

    def hasRoleGroup(self, groupName: str) -> bool:
        """Check if a role group with given name exists in the event."""
        return groupName in self.roleGroups

    def signup(self, roleToSet, user):
        """Add username to role."""
        for roleGroup in self.roleGroups.values():
            for role in roleGroup.roles:
                if role == roleToSet:
                    role.userID = user.id
                    role.userName = user.display_name

    def undoSignup(self, user) -> None:
        """Remove username from any signups."""
        for roleGroup in self.roleGroups.values():
            for role in roleGroup.roles:
                if role.userID == user.id:
                    role.userID = None
                    role.userName = ""
        return None

    def findSignup(self, userID) -> Role:
        """Check if given user is already signed up."""
        for roleGroup in self.roleGroups.values():
            for role in roleGroup.roles:
                if role.userID == int(userID):
                    return role
        return None

    def __str__(self):
        return "{} at {}".format(self.title, self.date)

    def toJson(self):
        roleGroupsData = {}
        for groupName, roleGroup in self.roleGroups.items():
            roleGroupsData[groupName] = roleGroup.toJson()

        data = {}
        data["title"] = self.title
        data["date"] = self.date.strftime("%Y-%m-%d")
        data["description"] = self.description
        data["time"] = self.date.strftime("%H:%M")
        data["terrain"] = self.terrain
        data["faction"] = self.faction
        data["color"] = self.color
        data["roleGroups"] = roleGroupsData
        return data

    def fromJson(self, data, guild):
        self.setTitle(data.get("title", TITLE))
        time = datetime.strptime(data.get("time", "00:00"), "%H:%M")
        self.setTime(time)
        self.setTerrain(data.get("terrain", TERRAIN))
        self.faction = data.get("faction", FACTION)
        self.description = data.get("description", DESCRIPTION)
        self.color = data.get("color", COLOR)
        # TODO: Handle missing roleGroups
        for groupName, roleGroupData in data["roleGroups"].items():
            roleGroup = RoleGroup(groupName)
            roleGroup.fromJson(roleGroupData, guild)
            self.roleGroups[groupName] = roleGroup
