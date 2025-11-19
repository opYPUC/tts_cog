import discord

from .tts_cog import TTSCog



def setup(bot: discord.Bot):
    bot.add_cog(TTSCog(bot))
