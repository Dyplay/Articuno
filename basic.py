import discord
from discord.ext import commands
import random


class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Ping the commands")
    async def ping(self, ctx):
        embed = discord.Embed(description=f":ping_pong:Pong! Took about {round(self.bot.latency * 1000)}ms", color=orange)
        await ctx.send(embed=embed)
    @commands.command(description="Avatar of a spetified user")
    async def avatar(self, ctx, *,  avamember : discord.Member=None):
        if not avamember:
          avamember = ctx.author
        avatar = avamember.avatar_url
        member = avamember.name
        embed = discord.Embed(description=f"**Avatar**", color=random.randint(0, 0xFFFFFF))
        embed.set_author(name=member, icon_url=avatar)
        embed.set_image(url=avatar)
        await ctx.send(embed=embed)
        

    
def setup(bot):
  bot.add_cog(Basic(bot))
