import discord
from discord.ext import commands
import DiscordUtils
import random

class Embeds:
    class Help:
        async def gen(self, help: commands.HelpCommand):
            ctx = help.context
            embeds = []
            color=random.randint(1, 16777215)
            p = 0
            ps = len(help.paginator.pages)
            for page in help.paginator.pages:
                p + 1
                e = discord.Embed(title='Help', description ='', color=color)
                e.description += f"{page}\n"
                if len(help.paginator.pages) <= 1:
                    await ctx.send(embed=e)
                    return None, None
                e.set_footer(text=f'Page {p}/{ps}')
                embeds.append(e)
            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, auto_footer=True)
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('⏹', "lock")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            return embeds, paginator