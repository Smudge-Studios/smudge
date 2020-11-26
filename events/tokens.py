from core.UtilCore import Utils
import re
import binascii
import base64
import mystbin
import discord
from discord.ext import commands

utils = Utils()
mystbin_client = mystbin.MystbinClient()
TOKEN_REGEX = re.compile(r'[a-zA-Z0-9_-]{23,28}\.[a-zA-Z0-9_-]{6,7}\.[a-zA-Z0-9_-]{27}')

def validate_token(token):
    try:
        # Just check if the first part validates as a user ID
        (user_id, _, _) = token.split('.')
        user_id = int(base64.b64decode(user_id, validate=True))
    except (ValueError, binascii.Error):
        return False
    else:
        return True

class TokenDetector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if utils.tokenon(message.guild.id):
            tokens = [token for token in TOKEN_REGEX.findall(message.content) if validate_token(token)]
            if tokens and message.author.id != self.bot.user.id:
                content = '\n'.join(tokens)
                paste = await mystbin_client.post(content, syntax="text")
                url = str(paste)
                try:
                    await message.channel.send(f"{message.author.mention} Tokens were found in your message. I have sent them to {url} to be invalidated.")
                except:
                    pass
            if utils.mistbinon(message.guild.id) == False:
                if len(message.attachments) >= 1:
                    filename = message.attachments[0].filename
                    _split = filename.split('.')
                    i = len(_split)-1
                    if _split[i] == 'txt':
                        attachment = message.attachments[0]
                        content = await attachment.read()
                        msg = content.decode("utf-8")
                        tokens = [token for token in TOKEN_REGEX.findall(msg) if validate_token(token)]
                        if tokens and message.author.id != self.bot.user.id:
                            content = '\n'.join(tokens)
                            paste = await mystbin_client.post(content, syntax="text")
                            url = str(paste)
                            try:
                                await message.channel.send(f"{message.author.mention} Tokens were found in your message. I have sent them to {url} to be invalidated.")
                            except:
                                pass

def setup(bot):
    bot.add_cog(TokenDetector(bot))