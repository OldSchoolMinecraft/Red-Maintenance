from typing import Literal

import discord
import datetime
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Maintenance(commands.Cog):
    """
    Allow admins to open maintenance windows.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=173495550467899402,
            force_registration=True,
        )
    
    @commands.command()
    @commands.admin()  # Restrict command to administrators
    async def maintenance(self, ctx, start_time, end_time, channel_id: int):
        """Sets a maintenance window with the given start and end times in the specified channel."""

        try:
            # Try parsing ISO 8601 format first
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
        except ValueError:
            # If ISO 8601 fails, try the custom format
            try:
                start_time = datetime.strptime(start_time, "%m/%d/%Y %H:%M")
                end_time = datetime.strptime(end_time, "%m/%d/%Y %H:%M")
            except ValueError:
                await ctx.send("Invalid time format. Please use ISO 8601 format (YYYY-MM-DDTHH:MM:SS) or MM/DD/YYYY HH:MM")
                return

        if start_time >= end_time:
            await ctx.send("Start time must be before end time.")
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            await ctx.send("Invalid channel ID.")
            return

        start_timestamp = f"<t:{int(start_time.timestamp())}:R>"
        end_timestamp = f"<t:{int(end_time.timestamp())}:R>"

        embed = discord.Embed(
            title="Maintenance Window",
            description="**A maintenance window has been opened!**",
            color=discord.Color.blue()
        )
        embed.add_field(name="Start Time", value=start_timestamp, inline=False)
        embed.add_field(name="End Time", value=end_timestamp, inline=False)
        embed.set_footer(text=f"Scheduled by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        await channel.send(embed=embed)
        await ctx.send("Maintenance window message sent successfully!")


    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)
