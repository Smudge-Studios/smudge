from aiohttp.client import ClientSession
import discord
from discord.ext import commands
import random
import time

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession()

    @commands.command()
    async def meme(self, ctx):
        """ Display a random meme from [r/memes](https://reddit.com/r/memes/). """
        color=random.randint(1, 16777215)
        async with ctx.channel.typing():
            while True:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    async with self.session.get('https://api.reddit.com/r/memes/top?limit=50', headers=headers) as response:
                        data = await response.json()
                    break
                except:
                    pass
            while True:
                postnum = random.randint(0, 50)
                try:
                    title = data['data']['children'][postnum]['data']['title']
                    image_url = data['data']['children'][postnum]['data']['url_overridden_by_dest']
                    post_id = data['data']['children'][postnum]['data']['id']
                    upvotes = data['data']['children'][postnum]['data']['ups']
                    break
                except IndexError:
                    pass
            embed = discord.Embed(title=title, url=f"https://www.reddit.com/r/memes/comments/{str(post_id)}", color=color)
            embed.set_image(url=image_url)
            embed.set_footer(icon_url='https://cdn.discordapp.com/emojis/781603344397500416.png?v=1', text=str(upvotes))
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)

    @commands.command()
    async def clap(self, ctx, *text):
        """ Put👏clap👏emojis👏between👏words. """
        if text == ():
            await ctx.reply('Please👏provide👏text👏for👏me👏to👏clap')
            return
        message = '👏'.join(text)
        await ctx.reply(message)

    @clap.error
    async def clap_error(self, ctx, error):
        """ When the clap command encounters an error. """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please👏provide👏text👏for👏me👏to👏clap')
        else:
            await ctx.reply('Please👏provide👏text👏for👏me👏to👏clap')

    @commands.command()
    async def hack(self, ctx, member: discord.Member=None):
        """ Hack someone. """
        if member is None:
            await ctx.reply('PL3453 M3NT10N S0M30N3 F0R M3 70 H4CK.')
            return
        message = await ctx.reply(f"Commencing hack on {member.name}.")
        time.sleep(3)
        await message.edit(content=f"Grabbing account details...")
        time.sleep(3)
        domains = ['gmail.com','yahoo.com','outlook.com','mail.com']
        domain = random.choice(domains)
        await message.edit(content=f"Email: {member.name}@{domain}\nPassword: ILoveMyMommy<3")
        time.sleep(3)
        await message.edit(content=f"Grabbing IP...")
        time.sleep(3)
        y = [192, 172, 10]
        a = random.choice(y)
        if a == 10:
            b = random.randint(0,255)
            c = random.randint(0,255)
            d = random.randint(0,255)
        elif a == 192:
            b = 168
            c = random.randint(0,255)
            d = random.randint(0,255)
        elif a == 172:
            b = random.randint(16,31)
            c = random.randint(0,255)
            d = random.randint(0,255)
        else:
            a = 172
            b = 20
            c = 185
            d = 73
        await message.edit(content=f"IP: {a}.{b}.{c}.{d}")
        time.sleep(3)
        await message.edit(content=f"Disabling email...")
        time.sleep(3)
        await message.edit(content=f"Issuing account deletion request...")
        time.sleep(3)
        await message.edit(content=f"Hack completed.")
        await ctx.reply("The 100% real and totally not fake hack was completed.")

    @commands.command(name='8ball')
    async def eightball(self, ctx, *, question):
        """ Ask the 8ball a question. """
        if question == '':
            await ctx.reply("You didn't ask me a question.")
            return
        msgs = ['As I see it, yes.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                "Concentrate and ask again.",
                "Don't count on it.",
                "It is certain.",
                'It is decidedly so.',
                "Most likely.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Outlook good.",
                "Reply hazy, try again.",
                "Signs point to yes.",
                "Very doubtful.",
                "Without a doubt.",
                "Yes.",
                "Yes ? definitely.",
                "You may rely on it."]
        msg = random.choice(msgs)
        await ctx.reply(msg)
    
    @eightball.error
    async def eightball_error(self, ctx, error):
        """ When 8ball encounters an error. """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("You didn't ask me a question.")
    
    @commands.command()
    async def imposter(self, ctx, imposter: str=None):
        """ Are they an imposter? """
        if imposter is None:
            imposter = f"<@{ctx.author.id}>"
        yn = random.choice(['was', 'was not'])
        await ctx.reply(f"""。　　　　•　 　ﾟ　　。。　　　　•　 　ﾟ　　。\n　　.　　　.　　　 　　.　　　　　。　　 。　.\n　.　 。　 ඞ 。　 . •。　　　　•　 　ﾟ　　。。　\n。　。•{imposter} {yn} An Imposter •. 。　.。　\n。　　　　•　 　ﾟ　　。。　　　　•　 　ﾟ　　。\n　　.　　　.　　　 　　.　　　　　。　　 。　.\n　.　 。　  。　 . •。　　　　•　 　ﾟ　　。。 . •。""")

    @commands.command()
    async def say(self, ctx, *, text: str=None):
        """ Make the bot say something. """
        if text is None:
            await ctx.reply("You must provide something for me to say.")
            return
        await ctx.reply(text)

def setup(bot):
    bot.add_cog(Fun(bot))