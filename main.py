import discord
import asyncio
import check_summoner
import ps_db;
import json;

client = discord.Client()

helpInfo = 'Hey!\nYou can type #test to test me.\nType in #check {summonername} to see if a buddy is in game. Type in #jinxed !'
db = ps_db.psdb()

@client.event
async def on_ready():
    print('Hi, I\'m logged in!')


@client.event
async def on_message(message):
    if message.content.startswith('#'):
        command = message.content[1:].lower()
        if command.startswith('help'):
            await client.send_message(message.channel, helpInfo)
        elif command.startswith('test'):
            await client.send_message(message.channel, 'You said test! Nice!')
        elif command.startswith('jinxed'):
            db.increase_jinxed()
            times = str(db.get_jinxed_times())
            await client.send_message(message.channel, 'Oh, you said jinxed? He\'s a total noob, trust me!\nI said that {0} times'.format(times))
        elif command.startswith('check'):
            try:
                status = check_summoner.check_if_summoner_ingame(command)
            except check_summoner.CouldNotFindSummonerException as e:
                await client.send_message(message.channel, 'I could not find this summoner, unfortunately.')
                return
            if status:
                response_message = 'Yo, that guy is in game!'
            else:
                response_message = 'He\'s not playing rn.'
            await client.send_message(message.channel, response_message)
        elif command.startswith('noob'):
            await client.send_message(message.channel, "Try #jinxed")
        else:
            await client.send_message(message.channel, 'I do not know this command. Try #help.')
client.run(json.loads(open('settings.json').read())["bot_code"])