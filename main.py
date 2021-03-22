from modules import getlink
import requests, discord, logging, git, os
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


bot = commands.Bot(command_prefix='/', description="Wikipedia Link Bot")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bu = baseURL()

@bot.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == bot.user:
        return
    if message.channel not in chans:
        chans.append(message.channel)
        if dirty():
            await message.channel.send("This bot is not in the stable state.")
    titles = getlink.gl(message.content)
    RTXT = ""
    for x in titles:
        RTXT = RTXT + bu.format(x) + "\n"
    if RTXT != "":
        await message.channel.send(RTXT)
    return

@bot.event
async def on_guild_join(G):
    await G.system_channel.send("Thank you for using this robot. When you enter `[[page name]]` or `{{template name}}`, the robot will automatically reply with a link.")

if __name__ == "__main__":
    bot.run(token())


        
