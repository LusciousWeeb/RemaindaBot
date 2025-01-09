import discord

class Client(discord.client):
    async def on_ready(self):
            print(f'Logged on as {self.user}!')


intents = discord.Intents.default()
intents.message_contet = True

client = Client(intents=intents)
client.run('MTMyNjY5MTczNDIzMDY2MzE3OA.GXXNUf.pSz_oV7Mpq3y_cgLSDTjFH4YjinfiRLwkrD7nU')