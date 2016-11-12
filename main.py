import discord
import asyncio
import check_summoner
import ps_db
import json
import subprocess
import os
import authorization
import re

client = discord.Client()

helpInfo = 'Hey!\nYou can type #test to test me.\nType in #check {summonername} to see if a buddy is in game.\nBy the way, be aware of #noob s. Type in #jinxed !\nCheck #commands for static commands.'
db = ps_db.psdb()
owner_id = int(json.loads(open('settings.json').read())["owner_id"])
admins = json.loads(open('settings.json').read())["admins"]
my_app_name = json.loads(open('settings.json').read())["app_name"]
@client.event
async def on_ready():
    print('Hi, I\'m logged in!')

def get_id(message):
    return message.author.id

@client.event
async def on_message(message):
    if message.content.startswith('#'):
        command = message.content[1:]
        matches = re.search('(?<=[a-z_A-Z] ).+', str(command))
        if not matches is None:
            args = matches.group(0)
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
        elif command.startswith('auth'):
            if authorization.is_owner(get_id(message)):
                await client.send_message(message.channel, 'Ok, you are the owner')
            elif authorization.is_admin(get_id(message)):
                await client.send_message(message.channel, 'Ok, you are the admin')
            else:
                await client.send_message(message.channel, 'Sorry, I don\'t know you')
        elif command.startswith('admins'):
            admins = authorization.get_admins(get_id(message))
            if admins is None:
                await client.send_message(message.channel, 'Sorry, I don\'t know you')
            response = "Admins are ";
            first = True
            for admin in admins:
                if not first:
                    response += ', '
                info = await client.get_user_info(admin)
                response = response + info.display_name
                first = False
                response += '.'
            await client.send_message(message.channel, response)
        elif command.startswith('add_admin'):
            user_name = args
            user = message.server.get_member_named(user_name)
            if user is None:
                await client.send_message(message.channel, 'Sorry, I could not find that guy')
                return;
            user_id = user.id
            res = authorization.add_admin(get_id(message), user_id)
            if res:
                await client.send_message(message.channel, 'Gotcha!')
            else:
                await client.send_message(message.channel, 'Sorry, I don\'t know you')
        elif command.startswith('delete_admin'):
            user_name = args
            user = message.server.get_member_named(user_name)
            if user is None:
                await client.send_message(message.channel, 'Sorry, I could not find that guy')
                return
            user_id = user.id
            res = authorization.delete_admin(get_id(message), user_id)
            if res:
                await client.send_message(message.channel, 'Gotcha!')
            else:
                await client.send_message(message.channel, 'Sorry, I don\'t know you')
        elif command.startswith('add_command'):
            if not authorization.is_admin(get_id(message)):
                await client.send_message(message.channel, 'Sorry, I don\'t know you')
            args_split = args.split(' ', 1)
            if(len(args_split) < 2):
                await client.send_message(message.channel, 'Sorry, incorrect format.')
                return
            name = args_split[0]
            msg = args_split[1]
            db.add_message(name, msg)
            await client.send_message(message.channel, 'Gotcha!')
        elif command.startswith('delete_command'):
            if not authorization.is_admin(get_id(message)):
                await client.send_message(message.channel, 'Sorry, I don\'t know you')
            db.delete_message(args)
            await client.send_message(message.channel, 'Gotcha!')
        elif command.startswith('commands'):
            messages = db.get_all_messages()
            first = True
            response = 'Static Commands: '
            for message_name in messages:
                if not first:
                    response += ', '
                response = response + message_name
                first = False
            response += '.'
            await client.send_message(message.channel, response)

        else:
            cmd_split = command.split(' ', 1)[0]
            msg = db.get_message(cmd_split)
            if msg is not None:
                await client.send_message(message.channel, msg)
                return;
            await client.send_message(message.channel, 'I do not know this command. Try #help.')


client.run(json.loads(open('settings.json').read())["bot_code"])