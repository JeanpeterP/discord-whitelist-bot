from asyncio import sleep
import argparse
import discord, datetime
import tweepy
from config import *

def parser():   
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", type=str, required=True)
    args = parser.parse_args()
    config_file = args.config_file
    return open(config_file).read()
    
exec(parser())

class Client(discord.Client):
    running = True

    async def twitterapi(self):
    # Replace these with your own API keys and secrets
        client_id = "X"
        client_secret = "X"
        consumer_key = "X"
        consumer_secret = "X"
        access_token = "X"
        access_token_secret = "X"
        bearer_token = "X"
        # Authenticate the request
        return tweepy.Client(consumer_key = consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret,bearer_token=bearer_token)

    async def twittercheck(self):
        api = await self.twitterapi()
        tweets_array = api.search_recent_tweets(query="giveaway" or "giveaways")

        for tweets in tweets_array:
            for tweet in tweets:
                try:
                    if isinstance(tweet.id, int):
                        api.retweet(tweet.id)
                        print("Tweet retweeted")
                    else:
                        continue
                except AttributeError:
                    continue
                    

    async def pause(self):
        self.running = False
        print("Bot paused.")

    async def continueBot(self):
        self.running = True
        print("Bot restored.")

    async def clean(self, user_message=None, bot_message=None):
        await sleep(3)
        if user_message is not None:
            await user_message.delete()
        if bot_message is not None:
            await bot_message.delete()
        print("Chat cleaned")

    async def send(self, ctx, content):
        message = await ctx.channel.send(f"{ctx.author.mention} {content}")
        print(f"Sent '{content}' to '{ctx.author}'")
        await self.clean(ctx, message)

    async def messageCheck(self):
        channels_ids = []
        for server in self.guilds:
            for channel in server.channels:
                if str(channel.type) == 'text':
                    channels_ids.append(channel.id)
        print(channels_ids)
        #channels_ids = [channel.id for channel in channels]
        # Get a list of all chanells in the current server
        for channel_id in channels_ids:
            channel = self.get_channel(channel_id)
            async for message in channel.history(limit=50):
                if message.author != self.user:
                    if "react" in message.content.lower():
                        await message.add_reaction("\N{THUMBS UP SIGN}")
        return 120
        # Code from original auto-bump author
    async def message(self):
        self.diff = await self.messageCheck()
        await sleep(self.diff)
        channel = self.get_channel(channel_id)
        command = await channel.send("Hi")
        print("Message sent")
        return command

    async def on_ready(self):
        print(f"Logged as {self.user}")
        while self.running == True:
            command = await self.message()
            await self.clean(command)

    async def on_message(self, message):
        if message.author == self.user:
            if message.content == "!pause":
                await self.pause()
                await self.send(message, "Bot is paused :sleeping:")

            elif message.content == "!continue":
                await self.continueBot()
                await self.send(
                    message,
                    f"Bump is activated, next bump in {self.diff} seconds :hourglass_flowing_sand:",
                )
            elif message.content == "!twitter":
                await self.twittercheck()

Client().run( user_token, bot=False)