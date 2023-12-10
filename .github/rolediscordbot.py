import discord
from bot_functions import *
from discord.ext import commands
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = get_intents()

client = commands.Bot(command_prefix="!", intents=intents)
role_selection_message = None

# Emojis and role descriptions
emoji_to_role = {
    '<:autonomous_vehicle:1148337868201267270>': 'Autonomous Vehicle Design Team',
    '<:kotlin:1148337119442518036>': 'Kotlin App',
    '<:swift:1148337328415322172>': 'Swift App',
    '<:leetcode:1148349688924340314>': 'Interview Prep',
}

role_descriptions = {
    'Autonomous Vehicle Design Team': 'if you are interested in participating in our Autonomous Vehicle design team',
    'Kotlin App': 'if you are interested in participating in our Kotlin Mobile App design team',
    'Swift App': 'if you are interested in participating in our Swift Mobile App design team',
    'Interview Prep': 'if you are interested in getting notified on our technical interview office hours'
}

@client.event
async def on_ready():
    global role_selection_message
    logger.info(f'Logged in as {client.user.name}')
    
    # Find "roles" channel
    role_selection_channel = discord.utils.get(client.guilds[0].text_channels, name="roles")

    # Checking for channel
    if role_selection_channel:
        # Check if there's an existing role selection message
        async for message in role_selection_channel.history(limit=1):
            if message.author == client.user:
                role_selection_message = message
                break
        
        if role_selection_message:
            logger.info(f'Found existing role selection message: {role_selection_message.jump_url}')
        else:
            # Create a new role selection message
            embed = discord.Embed(
                title="Design Team Roles",
                color=discord.Color.dark_gray()
            )

            # Add fields to the embed message
            for emoji, role_name in emoji_to_role.items():
                role = discord.utils.get(role_selection_channel.guild.roles, name=role_name)
                if role:
                    description = role_descriptions.get(role_name, '')
                    field_value = f"{emoji} {role.mention} - {description}" if description else f"{emoji} {role.mention}"
                    embed.add_field(name="", value=field_value, inline=False)


            # Send the embed message
            role_selection_message = await role_selection_channel.send(embed=embed)

            # Add reactions to the message
            for emoji in emoji_to_role.keys():
                await role_selection_message.add_reaction(emoji)

            logger.info(f'Created new role selection message: {role_selection_message.jump_url}')
        
        client.role_selection_message = role_selection_message

# Calls when a reaction is added to the role selection message
@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    # Check if the reaction is on the role selection message
    if reaction.message == client.role_selection_message:
        # Needed to convert emoji to string for custom emojis to compare with emoji_to_role dictionary keys
        if str(reaction.emoji) in emoji_to_role:
            role_name = emoji_to_role[str(reaction.emoji)]
            role = discord.utils.get(user.guild.roles, name=role_name)
            if role:
                await user.add_roles(role)

                if role_name == 'Autonomous Vehicle Design Team':
                    await user.send("""You have been assigned the Autonomous Vehicle Design Team role! Here you can find the 
                                    latest updates on our Autonomous Vehicle projects. If you are a member of this project, 
                                    please reach out to Lorenz Carvajal or Alex Lyew to join your team's channels!""")
                elif role_name == 'Kotlin App':
                    await user.send("""You have been assigned the Kotlin App role! Here you can find the latest updates on our 
                                    Android Mobile App project. If you are a member for this project, please reach out to Miguel 
                                    Tejeda to join your team's channels!""")
                elif role_name == 'Swift App':
                    await user.send("""You have been assigned the Swift App role! Here you can find the latest updates on our 
                                    iOS Mobile App project. If you are a member for this project, please reach out to Jesus Lopez 
                                    to join your team's channels!""")
                elif role_name == 'Interview Prep':
                    await user.send("""You have been assigned the Interview Prep role! Here you can join us in our technical 
                                    prep office hours, sign up for mock interviews and solve a LeetCode Question of the Week. 
                                    If you have any questions, feel free to reach out to Mateo Slivka, Santiago Barrios or 
                                    Diego Santos Gonzalez!""")
                    
# Calls when a reaction is removed from the role selection message
@client.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return

    if reaction.message == client.role_selection_message:
        if str(reaction.emoji) in emoji_to_role:
            role_name = emoji_to_role[str(reaction.emoji)]
            role = discord.utils.get(user.guild.roles, name=role_name)
            if role:
                await user.remove_roles(role)
                await user.send(f'You have removed the {role_name}.')

client.run(TOKEN)