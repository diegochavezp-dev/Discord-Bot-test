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
# COMANDO: WIKIDEX (Con tarjeta y borde amarillo)
# ==========================================
@bot.command(name="wikidex")
async def wikidex(ctx):
    """Envia la informacion dentro de un embed con borde amarillo"""
    
    descripcion = (
        "[WikiDex](<https://www.wikidex.net/wiki/WikiDex>), la enciclopedia Pokémon en español, "
        "se construye con aportaciones de fans como tú. Puedes ayudar haciendo correcciones de "
        "ortografía y otros fallos, ampliando información de juegos y productos oficiales, etc.\n\n"
        "🔸 Contacta con otros editores y recibe ayuda sobre cómo editar en nuestro Discord: "
        "https://discord.gg/nbqBprvpT 🔸"
    )
    
    # Creamos el embed. El color 16433152 es el amarillo WikiDex en decimal
    embed = discord.Embed(
        description=descripcion, 
        color=16433152
    )
    
    # Enviamos el embed al canal (ocultando cualquier otra previsualizacion extra)
    await ctx.send(embed=embed)

# ==========================================
# EVENTO DE ARRANQUE EN SILENCIO
# ==========================================
@bot.event
async def on_ready():
    print("Bot encendido correctamente. Modo tarjeta amarilla activado.")

bot.run(os.environ.get("DISCORD_TOKEN"))