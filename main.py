from modules import getlink
import requests, discord, logging, git, os, json, re
from discord.ext import commands
from git.exc import InvalidGitRepositoryError
log = logging.getLogger("MainScript" if __name__ == "__main__" else __name__)
chans = []

def dirty():
    fd = os.path.dirname(os.path.realpath(__file__))
    try:
        gr = git.Repo(fd)
    except InvalidGitRepositoryError:
        return false
    return gr.is_dirty(untracked_files=True)

def GFC(fname):
    try:
        with open(fname,"r") as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        log.error("No {}!".format(fname))
        return ""

def token():
    return GFC("token.txt")

def baseURL():
    return GFC("baseURL.txt")

def load():
    try:
        with open("config.json","r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        log.error("No config.json!")
        return {}

def save(cont):
    log.info("saving config with content:{}".format(str(cont)))
    with open("config.json","w+") as f:
        f.write(json.dumps(cont))


bot = commands.Bot(command_prefix='/', description="Wikipedia Link Bot", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bu = baseURL()

@bot.command()
async def conf(ctx, cname: str, value: str):
    if cname == "disable_link_reply":
        if value == "True" or value == "true":
            AVAL = True
            STAT = "Success"
        elif value == "False" or value == "false":
            AVAL = False
            STAT = "Success"
        else:
            AVAL = None
            STAT = "Failed"
    """ # TODO: allow optin or/and optout
    elif cname == "opt":
        if value == "False" or value == "false":
            AVAL = False
            STAT = "Disabled"
        else:
            try:
                re.compile(value)
                AVAL = value
                STAT = "Success"
            except re.error:
                AVAL = None
                STAT = "Regex Error"
    """
    else:
        AVAL = None
        STAT = "Invalid setting key"
    ALLC = load()
    try:
        CONF = ALLC[str(ctx.guild.id)]
    except KeyError:
        ALLC[str(ctx.guild.id)] = {}
        CONF = ALLC[str(ctx.guild.id)]
    if AVAL != None:
        CONF[cname] = AVAL
    save(ALLC)
    await ctx.send(STAT)

@bot.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == bot.user:
        return
    if message.channel not in chans:
        chans.append(message.channel)
        if dirty():
            await message.channel.send("This bot is not in the stable state.")
    ALLC = load()
    try:
        CONF = ALLC[str(message.channel.guild.id)]
    except KeyError:
        ALLC[str(message.channel.guild.id)] = {}
        CONF = ALLC[str(message.channel.guild.id)]
    try:
        if CONF["disable_link_reply"] == True:
            await bot.process_commands(message)
            return
    except KeyError:
        pass
    """ # TODO: allow optin or/and optout
    try:
        opt = CONF["opt"]
        if opt != False:
            if re.search(opt,message.content) == None:
                await bot.process_commands(message)
                return
    except KeyError:
        pass
    """
    titles = getlink.gl(message.content)
    RTXT = ""
    for x in titles:
        RTXT = RTXT + bu.format(x) + "\n"
    if RTXT != "":
        await message.channel.send(RTXT)
    await bot.process_commands(message)
    return
    

@bot.event
async def on_guild_join(G):
    await G.system_channel.send("Thank you for using this robot. When you enter `[[page name]]` or `{{template name}}`, the robot will automatically reply with a link.")

if __name__ == "__main__":
    bot.run(token())


        
