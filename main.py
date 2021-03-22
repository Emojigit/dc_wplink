from modules import getlink
import requests, discord, logging, git, os
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

class MyClient(discord.Client):
    def __init__(self,base):
        self.baseURL = base
        discord.Client.__init__(self)
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        if message.channel not in chans:
            chans.append(message.channel)
            if dirty():
                await message.channel.send("This bot is not in the stable state.")
        titles = getlink.gl(message.content)
        RTXT = ""
        for x in titles:
            RTXT = RTXT + self.baseURL.format(x) + "\n"
        if RTXT != "":
            await message.channel.send(RTXT)
        return
    async def on_guild_join(self,G):
        await G.system_channel.send("Thank you for using this robot. When you enter `[[page name]]` or `{{template name}}`, the robot will automatically reply with a link.")


if __name__ == "__main__":
    client = MyClient(baseURL())
    client.run(token())


        
