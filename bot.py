import discord
from discord.ext import commands
import json
import os


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Charger les portefeuilles des utilisateurs à partir d'un fichier JSON
if os.path.exists('wallets.json'):
    with open('wallets.json', 'r') as f:
        wallets = json.load(f)
else:
    wallets = {}

def save_wallets():
    with open('wallets.json', 'w') as f:
        json.dump(wallets, f, indent=4)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong.')

@bot.command()
async def hadrien(ctx):
    await ctx.send('sale merde')

@bot.command()
async def qui(ctx):
    await ctx.send('Personne a demandé, ta gueule et mange ton ratio')

@bot.command()
async def ratio(ctx):
    # Récupérer les messages précédents dans le canal
    messages = []
    async for message in ctx.channel.history(limit=2):
        messages.append(message)

    if len(messages) < 2:
        await ctx.send("Pas assez de messages dans l'historique pour déterminer l'utilisateur précédent.")
        return

    previous_message = messages[1]  # Le message avant la commande
    previous_user_tag = previous_message.author

    await ctx.send(f'Womp Womp {previous_user_tag}')


######################################################## Partie gestion de l'argent ########################################################

@bot.command()
async def balance(ctx):
    user_id = str(ctx.author.id)
    if user_id not in wallets:
        wallets[user_id] = 100  # Initialiser le portefeuille avec 100 unités de monnaie
        save_wallets()
    await ctx.send(f'{ctx.author.mention}, vous avez {wallets[user_id]} unités de monnaie.')

@bot.command()
async def addmoney(ctx, amount: int):
    if ctx.author.guild_permissions.administrator:
        user_id = str(ctx.author.id)
        if user_id not in wallets:
            wallets[user_id] = 100  # Initialiser le portefeuille avec 100 unités de monnaie
        wallets[user_id] += amount
        save_wallets()
        await ctx.send(f'{ctx.author.mention}, vous avez reçu {amount} unités de monnaie. Nouveau solde : {wallets[user_id]}.')
    else:
        await ctx.send(f'{ctx.author.mention}, vous n\'avez pas la permission d\'ajouter de la monnaie.')

@bot.command()
async def transfer(ctx, member: discord.Member, amount: int):
    sender_id = str(ctx.author.id)
    receiver_id = str(member.id)

    if sender_id not in wallets:
        wallets[sender_id] = 100  # Initialiser le portefeuille avec 100 unités de monnaie
    if receiver_id not in wallets:
        wallets[receiver_id] = 100  # Initialiser le portefeuille avec 100 unités de monnaie

    if wallets[sender_id] < amount:
        await ctx.send(f'{ctx.author.mention}, vous n\'avez pas assez de monnaie pour transférer {amount} unités.')
    else:
        wallets[sender_id] -= amount
        wallets[receiver_id] += amount
        save_wallets()
        await ctx.send(f'{ctx.author.mention} a transféré {amount} unités de monnaie à {member.mention}.')
        await member.send(f'Vous avez reçu {amount} unités de monnaie de la part de {ctx.author.mention}. Nouveau solde : {wallets[receiver_id]}.')



bot.run('Your-Discord-Secret')
