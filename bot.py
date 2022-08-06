#imports
import discord
from discord.ext import commands
import logging
from riotwatcher import TftWatcher, ApiError
from dotenv import load_dotenv
import os

#logging initalization
logging.basicConfig(level=logging.INFO)

#load apiKey
def configure():
    load_dotenv()
configure()
riotApiKey = os.getenv('riotApiKey')
discordApiKey = os.getenv('discordApiKey')

#riotApi initalization
watcher = TftWatcher(riotApiKey)
region = "NA1"

#bot
client = commands.Bot(command_prefix = '!')

@client.command(name='rank')
async def rank(ctx, summonerName):
    try:
        summonerInfo = watcher.summoner.by_name(region, summonerName)
        rankedStats = watcher.league.by_summoner(region, summonerInfo['id'])
        tier = [tier['tier'] for tier in rankedStats]
        tierStr = "".join(tier)
        rank = [rank['rank'] for rank in rankedStats]
        rankStr = "".join(rank)
        leaguePoints = [leaguePoints['leaguePoints'] for leaguePoints in rankedStats]
        leaguePointsStr = str(leaguePoints[0])
        await ctx.send(tierStr + " " + rankStr + " " + leaguePointsStr + " LP")
    except ApiError as err: 
        if err.response.status_code == 404:
            await ctx.send("Who are you searching for?")
        if err.response.status_code == 429:
            await ctx.send("Please wait () seconds before trying again".format(err.headers['Retry-After']))

client.run('discordApiKey')