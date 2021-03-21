from modules import getlink
import requests, discord, logging
log = logging.getLogger("MainScript" if __name__ == "__main__" else __name__)

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
        titles = getlink.gl(message.content)
        RTXT = ""
        for x in titles:
            RTXT = RTXT + self.baseURL.format(x)
        if RTXT != "":
            await message.channel.send(RTXT)
        return

if __name__ == "__main__":
    client = MyClient(baseURL())
    client.run(token())


        
