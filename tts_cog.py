import asyncio

import discord
import httpx
import pyttsx3
from discord.ext import commands

from stw import response


class TTSCog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.tts_server_url = "http://localhost:5000"

    async def download_tts_audio(self, text: str,speaker: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f'{self.tts_server_url}/generate-tts',
                    params={"text": text,"speaker": speaker},
                )

                if response.status_code != 200:
                    return None

                data = response.json()
                filename = data["filename"]

                audio_response = await client.get(
                    f"{self.tts_server_url}/audio/{filename}"
                )
                if audio_response.status_code != 200:
                    return

                with open(f"temp_{filename}", "wb") as f:
                    f.write(audio_response.content)
                return f"temp_{filename}"

            except Exception as exc:
                print(exc)
                return None
            return None

    @commands.command(name="music")
    async def play_music(self, ctx: commands.Context):
        if not ctx.author.voice:
            return await ctx.send("Ты не в войсе")

        voice_channel = ctx.author.voice.channel
        try:
            vp: discord.VoiceClient = await voice_channel.connect()  # voiceProtocol

            import os
            file = discord.FFmpegPCMAudio("music.mp3", executable=r"E:\ff\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe")
            vp.play(file)
        except Exception as e:
            await ctx.send(f"Ошибка {e}")

        return None

    @commands.command(name="tts")
    async def play_tts(self, ctx: commands.Context, *, word: str):

        if not ctx.author.voice:
            return await ctx.send("Ты не в войсе")

        voice_channel = ctx.author.voice.channel

        bot_is_playing = False
        for vc in ctx.bot.voice_clients:
            if vc.is_playing():
                bot_is_playing = True
                break

        if bot_is_playing:
            return await ctx.send("Я ещё не договорил в другом канале")

        else:
            speaker, word = word.split(" ",1)
            await self.download_tts_audio(word, speaker)

            vc: discord.VoiceClient = await voice_channel.connect()  # voiceClient

            try:
                import os
                file = discord.FFmpegPCMAudio("temp_tts_silero.wav",
                                              executable=r"E:\ff\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe")
                vc.play(file)
                while vc.is_playing():
                    await asyncio.sleep(0.1)
                await vc.disconnect()

            except Exception as e:
                await ctx.send(f"Ошибка {e}")

            return None
