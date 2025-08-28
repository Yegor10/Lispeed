from disnake.ext import commands
import disnake
import random

class EntertainmentCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.сat_gifs = ['https://media.tenor.com/4PXxgZON9NwAAAAj/cats-miskey-the-peacemaker.gif'
                    'https://media.tenor.com/wBdiOvp_JFIAAAAi/cat-cat-meme.gif'
                    'https://media.tenor.com/nSYuBMLsck8AAAAi/cute.gif'
                    ] 
        self.puppies_gifs = [
            'https://media1.tenor.com/m/htB1payjG3sAAAAC/elfenlied-wanta.gif'
            'https://media.tenor.com/Eltw6rmCSacAAAAi/pixel-dogs.gif'
            'https://media.tenor.com/AXoz_0MFJ58AAAAi/pawsum-playpawsum.gif'
        ]
    
    @commands.slash_command(description="U hug a member🤗")
    async def hug(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):

        embed = disnake.Embed(
            title=f"{inter.author} hugged {member}",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.red()
        )
        embed.set_image(url="https://media.tenor.com/9lRjN-Sr204AAAAi/anime-anime-hug.gif")
        await inter.response.send_message(embed=embed)
    @commands.slash_command(description="send a random cute cat photo.")
    async def meow(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(
            title=f"Meoooooow",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.purple()
        )
        embed.set_image(url=random.choice(self.cat_gifs))
        await inter.response.send_message(embed=embed)
    @commands.slash_command(description="send a random cute puppy photo")
    async def woof(self, inter: disnake.ApplicationCommandInteraction):
        
        embed = disnake.Embed(
            title=f"Woof woof woof",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.dark_blue()
        )
        embed.set_image(url=random.choice(self.puppies_gifs))
        await inter.response.send_message(embed=embed)
    

    @commands.slash_command(description="You can pat member with this command🐾")
    async def pat(self, inter:disnake.ApplicationCommandInteraction, member:disnake):
        embed = disnake.Embed(
            title=f"{inter.author} patted {member}",
            description=f"command called by {inter.author}",
            colour=disnake.Colour
        )