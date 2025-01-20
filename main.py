import discord
from datetime import datetime
import nest_asyncio
import csv
import asyncio
from discord.ext import commands, tasks
from discord import app_commands



nest_asyncio.apply() #Fixes runtime loop error
testGround = discord.Object(id=1330346094907101224) #sets up the discord bot to run in a specific server (TSB)
channel_id = 1330347313956257964
global channel
# region To Do List sorter
class WorkSorter:
    def __init__(self, name = 'default'):
        self.name = name
        self.assignments = ["Assignments"]
        self.courses = ["Courses"]
        self.readSaveFile()

    def work_adder(self, assignment, course):
        self.assignments.append(assignment)
        self.courses.append(course)
        with open('to_do_list.txt', mode="w", newline="", encoding="utf-8") as taskfile: #Appends data to the file
            writer = csv.writer(taskfile)
            writer.writerows(zip(self.assignments,self.courses))
        
        print(f"Data appended to 'to_do_list.txt' was successful. The data {self.assignments} and {self.courses}!\n")

    def work_formatter(self):
        if not self.assignments or not self.courses:
            return "There is nothing on your to-do list!"
            
        max_assignment_length = max(len(a) for a in self.assignments)
        max_courses_length = max(len(b) for b in self.courses)
        separator_width = 5
        work_list = f"{'Assignment':<{max_assignment_length}} {'-':^{separator_width}} {'Courses':>{max_courses_length}}\n" + ('-' * (max_assignment_length + separator_width + max_courses_length)) + '\n'
        for i in range(1,len(self.assignments)):
            work_list += (
                f"{self.assignments[i]:<{max_assignment_length}} {'-':^{separator_width}} {self.courses[i]:>{max_courses_length}}\n"
            )
        return work_list


    def getAssignment(self):
        return self.assignments


    def readSaveFile(self):
        with open('to_do_list.txt', newline='', mode='r') as taskfile:
            taskreader = csv.reader(taskfile, delimiter=',')
            tasklist = list(taskreader) #You can to turn the iterable csv file into list because you may only iterate through an iteratable csv file once
            self.assignments = [row[0] for row in tasklist]
            for j in self.assignments:
                print(j)
            self.courses = [row[1] for row in tasklist]
            for j in self.assignments:
                print(j)




# endregion
# region Start Up
class Client(commands.Bot):
    async def on_ready(self): #Just relays message into terminal
        global user
        user = WorkSorter()
        current_time = datetime.now()
        time_of_start = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(f'Logged on as {self.user}! \nThe time is {time_of_start}.') # Show that the bot is on by printing out bot name in terminal

        try:
            guild = discord.Object(id=1330346094907101224)
            synced = await self.tree.sync(guild=guild) #Syncs the development server to the bot
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print('Error syncing commands: {e}')



    async def on_message(self, message):
        if message.author == self.user:
            return


        if message.content.startswith('hello'):
            message_time = datetime.now()
            formatted_time = message_time.strftime("%Y-%m-%d %H:%M:%S")
            user.name = message.author #creates profile of user, only expects one user for now

            await message.channel.send(f'Hello, {user.name}, the time is {formatted_time}')


        elif message.content.isupper() and any(char.isalpha() for char in message.content):
            await message.channel.send(f"{message.author.mention}, stop crying!")


        print(f'Message from {message.author}: {message.content}')


    async def on_reaction_add(self, reaction, user):
            await reaction.message.channel.send('You reacted')
            


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents) #Apparently, command prefixes are outdated
channel = client.get_channel(channel_id)
# Allows to send message ^^^
# endregion
# Start to define slash commands






            
# region monkey business
@client.tree.command(name="helloo", description="Say hello!", guild=testGround) #Specifies name (Must be lowercase) and description of our slash command
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")


@client.tree.command(name="piss", description="Relays message", guild=testGround)
async def printer(interaction: discord.Interaction): # First variable name must match the name of command
   result = """```diff\n-piss 8===D\n```"""
   for x in range(6): 
        result = result + " " + result
        
        
   await interaction.response.send_message(result)

@client.tree.command(name='repeat', description= "Sends a message x times", guild=testGround)
async def repeat(interaction: discord.Interaction, message: str, number_of_times: int):
    channel = client.get_channel(channel_id)

    if channel is None:
        print("Channel Not found")
        return
    for x in range(number_of_times):
        await channel.send(message)
        await asyncio.sleep(3)


# endregion





@client.tree.command(name="display", description="List out all Assignments", guild=testGround)
async def display(interaction: discord.Interaction):
    await interaction.response.send_message(user.work_formatter())


@client.tree.command(name="add", description="A to-do list", guild=testGround)
async def add(interaction: discord.Interaction, assignment: str = "Null", course: str = "Peenar"):
   

   if (assignment in user.assignments) or (course in user.courses):
        await interaction.response.send_message("That is already in there, monkey")



   user.work_adder(assignment, course)

   result = f"""Hello, {interaction.user.mention}, Here are the assignments to do:
**__Assignment To Do:__**

""" + user.work_formatter()
   

   await interaction.response.send_message(result)







# region Discord Key
client.run('')

# endregion