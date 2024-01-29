import json
from pathlib import Path

from redbot.core.bot import Red

from .Maintenance import Maintenance




async def setup(bot: Red) -> None:
    await bot.add_cog(Maintenance(bot))
