import asyncio

import discord
import pyttsx3
from discord.ext import commands

class TTSCog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.command(name="music")
    async def play_music(self, ctx: commands.Context):
        if not ctx.author.voice:
            return await ctx.send("Ты не в войсе")

        voice_channel = ctx.author.voice.channel
        try:
            vp: discord.VoiceClient = await voice_channel.connect() #voiceProtocol

            import os
            file = discord.FFmpegPCMAudio("music.mp3",executable=r"E:\ff\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe")
            vp.play(file)
        except Exception as e:
            await ctx.send(f"Ошибка {e}")

        return None

    @commands.command(name="tts")
    async def play_tts(self, ctx:commands.Context, *, word: str):

        if not ctx.author.voice:
            return await ctx.send("Ты не в войсе")

        voice_channel = ctx.author.voice.channel

        #if ctx.voice_client:
        #    await ctx.send("Я ещё не договорил в другом канале")

        bot_is_playing = False
        for vc in ctx.bot.voice_clients:
            if vc.is_playing():
                bot_is_playing = True
                break

        if bot_is_playing:
            return await ctx.send("Я ещё не договорил в другом канале")

        else:
            engine = pyttsx3.init()
            engine.save_to_file(word, 'tts_file.mp3')
            engine.runAndWait()

            vc: discord.VoiceClient = await voice_channel.connect()  # voiceClient

            try:
                import os
                file = discord.FFmpegPCMAudio("tts_file.mp3",executable=r"E:\ff\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe")
                vc.play(file)
                while vc.is_playing():
                    await asyncio.sleep(0.1)
                await vc.disconnect()

            except Exception as e:
                await ctx.send(f"Ошибка {e}")

            return None