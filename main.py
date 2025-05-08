'''
Si estás viendo este código, es algo viejo y solo lo subí por una prueba
'''

import discord
from discord.ext import commands
import os
import serversito
# from config import TOKEN

# DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="f!", intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"¡{bot.user.name} está en línea!")

    activity = discord.Game(name="I'm funny (estoy funado)")
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    author_top_role = ctx.author.top_role
    member_top_role = member.top_role

    if author_top_role <= member_top_role:
        await ctx.send("No puedes banear a un usuario con un nivel de rol mayor al tuyo.")
        return
    
    if author_top_role == member_top_role:
        await ctx.send("No puedes banear a un usuario con el mismo nivel de rol que el tuyo")
        return

    bot_top_role = ctx.guild.me.top_role
    if bot_top_role <= member_top_role:
        await ctx.send("No puedo banear a un usuario con un nivel de roles mayor o igual al mío.")
        return
    
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("No tienes permisos para usar este comando. Te voy a funar.")
        return
    
    embed = discord.Embed(title="Has sido baneado",
                          description=f"> **Servidor:** {ctx.guild.name}\n"
                                      f"> **Acción tomada por:** {ctx.author.mention}\n"
                                      f"> **Motivo:** {reason}",
                          color=discord.Color.red())
    embed.set_footer(text="Para más información, contacta al staff del servidor.")

    try:
        await member.send(embed=embed)
        await member.ban(reason=reason)
    except discord.HTTPException:
        await ctx.send("No se pudo enviar un mensaje privado al usuario baneado.")
    
    await ctx.send(f'{member.mention} ha sido baneado.')

## BAN SLASH 

@bot.tree.command(name="ban", description="Banea a un usuario del servidor.")
@discord.app_commands.describe(user="El usuario a banear", reason="Razón del baneo")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No se proporcionó razón"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("No tienes permisos para banear miembros.", ephemeral=True)
        return
    try:
        await user.ban(reason=reason)
        await interaction.response.send_message(f"El usuario {user.mention} ha sido baneado por: {reason}.")
    except Exception as e:
        await interaction.response.send_message(f"No se pudo banear al usuario. Error: {e}")

bot.run(DISCORD_TOKEN)
