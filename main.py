
# Some imports
from datetime import datetime
from interactions import discord_interactions, message
from discord.ext import commands
import discord
import json
import requests

config_file = open("bot_config.json", "r")
config_data = json.load(config_file)
config_file.close()

intents = discord.Intents()
intents.message_content=True
intents.messages=True
intents.members=True
intents.guilds=True

bot = commands.Bot(command_prefix=config_data['bot_prefix'], intents=intents,enable_debug_events=True)
bot.remove_command("help")

inter=discord_interactions.interactions(config_data['bot_token'], config_data['client_id'])

@bot.event
async def on_ready():
    print("Bot is ready")


@bot.event
async def on_socket_raw_receive(msgs):
    msg=json.loads(msgs)
    if msg['t']=="INTERACTION_CREATE":
        data=msg['d']
        ctx=inter.interaction_response(data, inter, bot)

        # print(msg)

        if ctx.type==3: # Buttons, the only one we actually need
            

            if ctx.custom_id=='hunt_role':
                ctx.interact.load(64)

                roles = ctx.raw['member']['roles']
                guild = bot.get_guild(int(ctx.raw['guild_id']))
                member = guild.get_member(int(ctx.raw['member']['user']['id']))

                s_roles=[]
                r=config_data['hunt_role']['role_id']
                role = guild.get_role(r)
                if not str(r) in roles:
                    await member.add_roles(role)
                    ctx.interact.edit_response(config_data['hunt_role']['role_add_msg'])
                else:
                    await member.remove_roles(role)
                    ctx.interact.edit_response(config_data['hunt_role']['role_rmv_msg'])


                


@bot.command(name="load_song-hunt_role")
@commands.has_permissions(administrator=True)
async def load_roles(ctx):
    """Loads the roles messages"""
    c=0
    comp = []
    msg = {
        "content": config_data['hunt_role']['message_content'], 
        "components": message.components.action_row([
            message.components.button(
                3,
                config_data['hunt_role']['button_label'],
                message.components.emoji(None),
                f"hunt_role"
            )
        ]).data
    }
    re = requests.post(
        f"https://discord.com/api/channels/{ctx.channel.id}/messages",
        json=msg,
        headers={"Authorization": f"Bot {config_data['bot_token']}"}
    )
    try: re.raise_for_status()
    except:
        await ctx.send(f"There was an error while sending the message\n`{re.text}`")
        return
    await ctx.message.delete()

@bot.command(name="help")
@commands.has_permissions(administrator=True)
async def help(ctx):
    """Get a list of my commands"""
    cnt=""
    for cmd in bot.commands:
        cnt += f"\n{config_data['bot_prefix']}{cmd.name:<20} | {cmd.help}"
    
    await ctx.send(f"My Commands:```{cnt}```")


@bot.event
async def on_command_error(err, err1):return

bot.run(config_data['bot_token'])