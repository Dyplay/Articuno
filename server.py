import discord
from discord.ext import commands
from discord.ext.commands import Greedy
from discord import User
import asyncio
from typing import Union
import requests



blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12
yellow = 0xfff900
gray = 0x6d6868

class Server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="About the channel", aliases=['serverinfo'])
    async def server(self, ctx):
        name = str(ctx.guild.name)
        id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        memberer = 0
        for member in ctx.guild.members:
            if not member.bot:
                memberer += 1
        if ctx.invoked_subcommand is None:
            bots = sum(1 for member in ctx.guild.members if member.bot)
        icon = str(ctx.guild.icon_url)
        owner = str(ctx.guild.owner.id)
        region = str(ctx.guild.region)
        created = str(ctx.guild.created_at.strftime("%B %d, %Y"))
        boost = ctx.guild.premium_subscription_count
        if boost <= 2:
            comment = "Level 0"
        if 2 <= boost < 15:
            comment = "Level 1"
        if 15 <= boost < 30:
            comment = "Level 2"
        if boost >= 30:
            comment = "Level 3"
        text_channel = len(ctx.guild.text_channels)
        voice_channel = len(ctx.guild.voice_channels)
        verify_level = ctx.guild.verification_level

        embed = discord.Embed(title=name + " Information", color=blue)
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Server ID :id:", value=id, inline=True)
        embed.add_field(name="Owner :crown:", value=f"<@{owner}>\nID: {owner}", inline=True)
        embed.add_field(name="Boost :gem:", value=f"Number: {boost}\n{comment}",inline=True)
        embed.add_field(name="Member :busts_in_silhouette:", value=f"Total: {memberCount}\nHumans: {memberer}\nBOTs: {bots}", inline=True)
        embed.add_field(name="Channels :keyboard:", value=f"<:text_channel:873442091424944178>Text channels: {text_channel}\n<:voice_channel:873442207758159904>Voice channels: {voice_channel}")
        embed.add_field(name="Region :globe_with_meridians:", value=region, inline=True)
        embed.add_field(name="Created on :clock1:", value=created, inline=True)
        embed.add_field(name="Verify level :shield:", value=f"Level: {verify_level}")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)



    @commands.command(description="Gets info about a specified user",aliases=['userinfo', 'whois', 'user'])
    async def info(self, ctx, member : discord.Member=None):
        if not member:
          member = ctx.author
        profile = member.public_flags
        hypesquad = "None"
        if profile.hypesquad_bravery == True:
                hypesquad = "<:bravery:875411242917969961> Bravery"
        if profile.hypesquad_brilliance == True:  
                hypesquad = "<:brilliance:875411403413000233> Brilliance"        
        if profile.hypesquad_balance == True:
                hypesquad = "<:balance:875411281350369330> Ballance"
        supporter = "No"
        if profile.early_supporter == True:
            supporter = "<:earlysupporter:875412600341540874> Yes"
        if not member.bot:
            bot = "No"
        else:
            bot = "Yes"
        color = member.top_role.color
        embed=discord.Embed(title="User info", colour=color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined on", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Top role", value=f"<@&{member.top_role.id}>", inline=True)
        embed.add_field(name="Created on", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Hypesquad", value=f"{hypesquad}")
        embed.add_field(name="Bot?", value=bot)
        embed.add_field(name="Early Supporter?", value=supporter)
        embed.set_footer(icon_url=member.avatar_url, text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    

    @commands.command(description="DM yourself")
    async def dm(self, ctx, *, message):
      try:
        embed = discord.Embed(title=f"Here is the message:", description=f"{message}", color=green)
        await ctx.author.send(embed=embed)
        await ctx.message.add_reaction("✅")
        await ctx.channel.send(':white_check_mark: Message delivered successfully')
      except:
        await ctx.message.add_reaction("❌")
        await ctx.channel.send(f"{ctx.author.mention}, your DM is closed. I can't deliver the message to you")


    @commands.command(description="*For admin only*: DM a group of member")
    @commands.has_permissions(administrator = True)
    async def message(self, ctx, users: Greedy[User], *, message):
      try:
        for user in users:
            embed = discord.Embed(title=f"From {ctx.author.name}", description=f"**Here is the message:** {message}", color=green)
            await user.send(embed=embed)
            await ctx.message.add_reaction("✅")
            await ctx.channel.send(":white_check_mark: Message delivered sccessfully")
      except:
        await ctx.message.add_reaction("❌")
        await ctx.channel.send("❌ The user has DM closed. I can't deliver the message")
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount=5):
      if amount >= 101:
        await ctx.send("Uh, I only allow you to delete 100 messages a time")
      else:
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount, bulk=True)
        message0 = await ctx.send(f"{amount} messages have been deleted. This message will be deleted after 3 seconds.")
        await asyncio.sleep(3)
        await message0.delete()

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def emojisteal(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji], name=None):
        if not name:
          name = emoji.name
        await ctx.guild.create_custom_emoji(name=name, image=await emoji.url.read())
        await ctx.send(f"Successfully added the emoji ``[:{name}:]``")

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def emojiadd(self, ctx, url, name):
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
            return await ctx.send("The URL you have provided is invalid.")
        if response.status_code == 404:
            return await ctx.send("The URL you have provided leads to a 404.")
        try:
            await ctx.guild.create_custom_emoji(name=name, image=response.content)
        except discord.InvalidArgument:
            return await ctx.send("Invalid image type. Only PNG, JPEG and GIF are supported.")
        await ctx.send(f"Successfully added the emoji ``[:{name}:]``")


    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def emojiremove(self, ctx, name):
        emotes = [x for x in ctx.guild.emojis if x.name == name]
        emote_length = len(emotes)
        if not emotes:
            return await ctx.send("No emotes with that name could be found on this server.")
        for emote in emotes:
            await emote.delete()
        if emote_length == 1:
            await ctx.send("Successfully removed the {} emoji!".format(name))
        else:
            await ctx.send("Successfully removed {} emoji with the name {}.".format(emote_length, name))

    @commands.command()
    async def emojiurl(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji]):
        await ctx.send(f"<{emoji.url}>")





def setup(bot):
    bot.add_cog(Server(bot))
    
