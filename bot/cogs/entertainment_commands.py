from disnake.ext import commands
import disnake
import random

class EntertainmentCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cat_gifs = [
            'https://media.tenor.com/4PXxgZON9NwAAAAj/cats-miskey-the-peacemaker.gif',
            'https://media.tenor.com/wBdiOvp_JFIAAAAi/cat-cat-meme.gif',
            'https://media.tenor.com/nSYuBMLsck8AAAAi/cute.gif'
        ] 
        self.puppies_gifs = [
            'https://media1.tenor.com/m/htB1payjG3sAAAAC/elfenlied-wanta.gif',
            'https://media.tenor.com/Eltw6rmCSacAAAAi/pixel-dogs.gif',
            'https://media.tenor.com/AXoz_0MFJ58AAAAi/pawsum-playpawsum.gif'
        ]
        self.kiss_gifs = [
            "https://media.tenor.com/huBeO_j21zYAAAAi/iphone-12-emojis.gif",
            "https://media.tenor.com/Tb5oi-FdAg0AAAAi/fofo-cute.gif",
            "https://media.tenor.com/2tlTR6jscocAAAAi/kiss-bubu-dudu.gif"
        ]
        self.punch_gifs = [
            "https://media.tenor.com/6W0qB3swv-0AAAAi/punch-smack.gif",
            "https://media.tenor.com/0D3YkN2o4o4AAAAi/punch-anime.gif",
            "https://media.tenor.com/6g8aCM4b0dUAAAAi/punch-fight.gif"
        ]
        self.dance_gifs = [
            "https://media.tenor.com/3QGY5jD2b1YAAAAi/dance-party.gif",
            "https://media.tenor.com/8y8hF3oq8eUAAAAi/dance-happy.gif",
            "https://media.tenor.com/k1oL1Z3X4d0AAAAi/dance-cute.gif"
        ]
        self.highfive_gifs = [
            "https://media.tenor.com/0VLJ6vXz2cEAAAAi/high-five.gif",
            "https://media.tenor.com/7b9g5Z5z5zYAAAAi/high-five-anime.gif",
            "https://media.tenor.com/XjZ7e4Z3Z3wAAAAi/high-five-teamwork.gif"
        ]
        self.cry_gifs = [
            "https://media.tenor.com/2vL6oJ3W3cYAAAAi/cry-sad.gif",
            "https://media.tenor.com/9Yg5b3Z3Z3wAAAAi/crying-anime.gif",
            "https://media.tenor.com/k5z6Y6z6Y6YAAAAi/sad-tears.gif"
        ]
        self.laugh_gifs = [
            "https://media.tenor.com/5Z3X5Z3X5Z3AAAAi/laugh-funny.gif",
            "https://media.tenor.com/8k2oL2oL2oLAAAAi/laughter-anime.gif",
            "https://media.tenor.com/7Y7bY7bY7bYAAAAi/laugh-happy.gif"
        ]
        self.sleep_gifs = [
            "https://media.tenor.com/9X9x9X9x9X9AAAAi/sleep-cute.gif",
            "https://media.tenor.com/4Z4z4Z4z4Z4AAAAi/sleeping-anime.gif",
            "https://media.tenor.com/3Y3y3Y3y3Y3AAAAi/sleep-tired.gif"
        ]
        self.eat_gifs = [
            "https://media.tenor.com/6T6t6T6t6T6AAAAi/eat-food.gif",
            "https://media.tenor.com/5R5r5R5r5R5AAAAi/eating-anime.gif",
            "https://media.tenor.com/4Q4q4Q4q4Q4AAAAi/eat-yummy.gif"
        ]
        self.run_gifs = [
            "https://media.tenor.com/2W2w2W2w2W2AAAAi/run-fast.gif",
            "https://media.tenor.com/1X1x1X1x1X1AAAAi/running-anime.gif",
            "https://media.tenor.com/0Y0y0Y0y0Y0AAAAi/run-away.gif"
        ]
        self.fly_gifs = [
            "https://media.tenor.com/8S8s8S8s8S8AAAAi/fly-superhero.gif",
            "https://media.tenor.com/7R7r7R7r7R7AAAAi/flying-anime.gif",
            "https://media.tenor.com/6Q6q6Q6q6Q6AAAAi/fly-sky.gif"
        ]
        self.magic_gifs = [
            "https://media.tenor.com/5P5p5P5p5P5AAAAi/magic-spell.gif",
            "https://media.tenor.com/4O4o4O4o4O4AAAAi/magic-anime.gif",
            "https://media.tenor.com/3N3n3N3n3N3AAAAi/magic-wand.gif"
        ]
        self.sing_gifs = [
            "https://media.tenor.com/2M2m2M2m2M2AAAAi/sing-mic.gif",
            "https://media.tenor.com/1L1l1L1l1L1AAAAi/singing-anime.gif",
            "https://media.tenor.com/0K0k0K0k0K0AAAAi/sing-song.gif"
        ]
        self.wave_gifs = [
            "https://media.tenor.com/9W9w9W9w9W9AAAAi/wave-hello.gif",
            "https://media.tenor.com/8V8v8V8v8V8AAAAi/waving-anime.gif",
            "https://media.tenor.com/7U7u7U7u7U7AAAAi/wave-hi.gif"
        ]
        self.thumbsup_gifs = [
            "https://media.tenor.com/6T6t6T6t6T6AAAAi/thumbs-up.gif",
            "https://media.tenor.com/5R5r5R5r5R5AAAAi/thumbsup-anime.gif",
            "https://media.tenor.com/4Q4q4Q4q4Q4AAAAi/thumbs-up-cool.gif"
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
    async def pat(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(
            title=f"{inter.author} patted {member}",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.green()
        )
        embed.set_image(url="https://placeholder-pat-gif-url-here.gif")  # Insert your pat GIF URL here
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Kiss a member 💋")
    async def kiss(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(
            title=f"{inter.author} kissed {member}",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.pink()
        )
        embed.set_image(url=random.choice(self.kiss_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Playfully punch a member 👊")
    async def punch(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(
            title=f"{inter.author} punched {member} (playfully!)",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.orange()
        )
        embed.set_image(url=random.choice(self.punch_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Dance with a member 💃🕺")
    async def dance(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(
            title=f"{inter.author} is dancing with {member}",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.yellow()
        )
        embed.set_image(url=random.choice(self.dance_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="High five a member ✋")
    async def highfive(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(
            title=f"{inter.author} high-fived {member}",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.blue()
        )
        embed.set_image(url=random.choice(self.highfive_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Send a crying reaction 😢")
    async def cry(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=f"{inter.author} is crying",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.teal()
        )
        embed.set_image(url=random.choice(self.cry_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Send a laughing reaction 😂")
    async def laugh(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=f"{inter.author} is laughing",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.gold()
        )
        embed.set_image(url=random.choice(self.laugh_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Send a sleeping reaction 😴")
    async def sleep(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=f"{inter.author} is sleeping",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.dark_purple()
        )
        embed.set_image(url=random.choice(self.sleep_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Send an eating reaction 🍔")
    async def eat(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=f"{inter.author} is eating",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.brown()
        )
        embed.set_image(url=random.choice(self.eat_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Run away from a member 🏃")
    async def run(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(
            title=f"{inter.author} is running away from {member}",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.light_grey()
        )
        embed.set_image(url=random.choice(self.run_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Fly like a superhero 🦸")
    async def fly(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=f"{inter.author} is flying",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.dark_blue()
        )
        embed.set_image(url=random.choice(self.fly_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Perform magic on a member ✨")
    async def magic(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(
            title=f"{inter.author} performed magic on {member}",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.magenta()
        )
        embed.set_image(url=random.choice(self.magic_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Sing a song 🎤")
    async def sing(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=f"{inter.author} is singing",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.red()
        )
        embed.set_image(url=random.choice(self.sing_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Wave at a member 👋")
    async def wave(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(
            title=f"{inter.author} waved at {member}",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.green()
        )
        embed.set_image(url=random.choice(self.wave_gifs))
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Give thumbs up 👍")
    async def thumbsup(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=f"{inter.author} gives thumbs up",
            description=f"Command called by {inter.author}",
            colour=disnake.Colour.blue()
        )
        embed.set_image(url=random.choice(self.thumbsup_gifs))
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(EntertainmentCommands(bot))