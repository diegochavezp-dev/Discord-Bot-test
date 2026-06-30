import os
import discord
from discord.ext import commands
from datetime import datetime, timezone

# 1. Configuracion de permisos logicos del Bot
intents = discord.Intents.default()
intents.message_content = True  
intents.reactions = True      
intents.members = True        
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables de control: Paypal apagado temporalmente
MAX_ENVIOS = 24
contador_envios = 0

# ==========================================
# COMANDO 1: WIKIDEX
# ==========================================
@bot.command(name="wikidex")
async def wikidex(ctx):
    """Envia el embed de WikiDex con el link crudo al final de la descripcion"""
    descripcion = (
        "[WikiDex](<https://www.wikidex.net/wiki/WikiDex>), la enciclopedia Pokémon en español, "
        "se construye con aportaciones de fans como tú. Puedes ayudar haciendo correcciones de "
        "ortografía y otros fallos, ampliando información de juegos y productos oficiales, etc.\n\n"
        "🔸 Contacta con otros editores y recibe ayuda sobre cómo editar en nuestro Discord: 🔸\n"
        "https://discord.gg/nbqBprvpT"
    )
    
    embed = discord.Embed(
        description=descripcion, 
        color=16433152 # Amarillo WikiDex
    )
    
    await ctx.send(embed=embed)

# ==========================================
# COMANDO 2: ANIVERSARIO PUEBLO PALETA
# ==========================================
@bot.command(name="aniversario")
async def aniversario(ctx):
    """Envia el anuncio de aniversario con la estructura exacta de la captura"""
    descripcion = (
        "¡**Pueblo Paleta** celebra su 3.er aniversario en julio! Eventos, sorpresas y "
        "buen ambiente te esperan. ¡Únete al servidor y celebra con nosotros! "
        "<:quagwin:1271553155108442125>\n\n"
        "https://discord.gg/vbpSZEevtv" # El link crudo directo, tal como en tu captura
    )
    
    embed = discord.Embed(
        description=descripcion,
        color=3447003 # Azul estándar de Discord
    )
    
    await ctx.send(embed=embed)

# ==========================================
# EVENTO DE ARRANQUE EN SILENCIO
# ==========================================
@bot.event
async def on_ready():
    print("Bot encendido. Comandos configurados con el link crudo interno.")

bot.run(os.environ.get("DISCORD_TOKEN"))