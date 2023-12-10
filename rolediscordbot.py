import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.reactions = True
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)
role_selection_message = None

@client.event
async def on_ready():
    global role_selection_message
    print(f'Logged in as {client.user.name}')
    
    # Find "roles-selection" channel
    role_selection_channel = discord.utils.get(client.guilds[1].text_channels, name="roles-selection")

    # Checking for channel
    if role_selection_channel:
        # Check if there's an existing role selection message
        async for message in role_selection_channel.history(limit=1):
            if message.author == client.user:
                role_selection_message = message
                break
        
        if role_selection_message:
            print(f'Found existing role selection message: {role_selection_message.jump_url}')
        else:
            # Create a new role selection embed message
            embed = discord.Embed(
                title="Role Selection:",
                description="React to any of the roles to get the one you want.",
                color=discord.Color.blue()
            )

            # Custom emojis id's and role names dictionary
            emoji_to_role = {
                '<:comp:1173517373278523412>': 'Computer Role',
                '<:linux:1173517388680011776>': 'Linux Role',
                '<:py:1173518516125708308>': 'Python Role',
            }

            # Add fields to the embed message
            for emoji, role_name in emoji_to_role.items():
                role = discord.utils.get(role_selection_channel.guild.roles, name=role_name)
                if role:
                    embed.add_field(name=emoji, value=role.mention, inline=True)

            # Send the embed message
            role_selection_message = await role_selection_channel.send(embed=embed)

            # Add reactions to the message
            for emoji in emoji_to_role.keys():
                await role_selection_message.add_reaction(emoji)

            print(f'Created new role selection message: {role_selection_message.jump_url}')
        
        client.role_selection_message = role_selection_message

# Calls when a reaction is added to the role selection message
@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    # Check if the reaction is on the role selection message
    if reaction.message == client.role_selection_message:
        emoji_to_role = {
            '<:comp:1173517373278523412>': 'Computer Role',
            '<:linux:1173517388680011776>': 'Linux Role',
            '<:py:1173518516125708308>': 'Python Role',
        }

        # Needed to convert emoji to string for custom emojis to compare with emoji_to_role dictionary keys
        if str(reaction.emoji) in emoji_to_role:
            role_name = emoji_to_role[str(reaction.emoji)]
            role = discord.utils.get(user.guild.roles, name=role_name)
            if role:
                await user.add_roles(role)

                if role_name == 'Computer Role':
                    await user.send('You selected the Computer Role! You will be coding and gaining experience on how computers function!')
                elif role_name == 'Linux Role':
                    await user.send('You selected the Linux Role! You will be learning about the possibilities of the Linux operating system!')
                elif role_name == 'Python Role':
                    await user.send('You selected the Python Role! You will be working on projects and exploring the potential of the Python coding language!')

# Calls when a reaction is removed from the role selection message
@client.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return

    if reaction.message == client.role_selection_message:
        emoji_to_role = {
            '<:comp:1173517373278523412>': 'Computer Role',
            '<:linux:1173517388680011776>': 'Linux Role',
            '<:py:1173518516125708308>': 'Python Role',
        }

        if str(reaction.emoji) in emoji_to_role:
            role_name = emoji_to_role[str(reaction.emoji)]
            role = discord.utils.get(user.guild.roles, name=role_name)
            if role:
                await user.remove_roles(role)
                await user.send(f'You have removed the {role_name}.')

client.run('MTE1NTcxMzExMzQ4MDUwMzMwNg.GBV3E-.XAzKwGbju8cjOeS7uLq3yz2rfhvAp669Lqg-4Y')