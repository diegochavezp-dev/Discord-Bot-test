import os
import discord
from discord.ext import commands, tasks
import asyncio

# 1. Configuración de permisos lógicos del Bot
intents = discord.Intents.default()
intents.message_content = True  
intents.reactions = True      
intents.members = True        
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables de control para la automatización (Pausadas temporalmente)
MAX_REPETICIONES = 8
contador_wikidex = 0
contador_aniversario = 0
toca_wikidex = True

# ==========================================
# TEXTOS Y EMBEDS CONFIGURADOS
# ==========================================
def obtener_embed_wikidex():
    descripcion = (
        "[WikiDex](<https://www.wikidex.net/wiki/WikiDex>), la enciclopedia Pokémon en español, "
        "se construye con aportaciones de fans como tú. Puedes ayudar haciendo correcciones de "
        "ortografía y otros fallos, ampliando información de juegos y productos oficiales, etc.\n\n"
        "🔸 Contacta con otros editores y recibe ayuda sobre cómo editar en nuestro Discord: 🔸\n"
        "https://discord.gg/nbqBprvpT"
    )
    return discord.Embed(description=descripcion, color=16433152)

def obtener_embed_aniversario():
    descripcion = (
        "¡**Pueblo Paleta** celebra su 3.er aniversario en julio! Eventos, sorpresas y "
        "buen ambiente te esperan. ¡Únete al servidor y celebra con nosotros! "
        "<:quagwin:1271553155108442125>\n\n"
        "Discord: https://discord.gg/vbpSZEevtv"
    )
    return discord.Embed(description=descripcion, color=16515241)

def obtener_embed_eventos():
    descripcion = (
        "¿Mucho vacío con los torneos? ¿quieres algo más allá de presionar botones contra el oponente? "
        "¿Cansado de scouting, haxing y schedule? ¡[Eventos](<https://play.pokemonshowdown.com/eventos>) es lo que necesitas! "
        "La sala que da eventos y torneos exclusivos por dinero, CAVY, recompensas como tarjetas de steam o la sencilla "
        "gloria de vencer a un tryhard y alimentar tu ego... Podrás hacer tus propios mons en el SSB, vencer desafíos en "
        "equipo en el CAMP, poner tu inteligencia a prueba en la Torre y tener acceso privilegiado a torneos para eventinos. "
        "La comunidad te espera con los brazos abiertos, ¡[Eventos](<https://play.pokemonshowdown.com/eventos>) espera tu desafío!\n\n"
        "¡Unete al Servidor NO oficial de Eventos, [Eventos Today](https://discord.gg/JTNPehs3c) donde podrás interactuar, "
        "shitpostear y divertirte con nosotros!\n\n"
        "Discord: https://discord.gg/JTNPehs3c"
    )
    return discord.Embed(description=descripcion, color=5641372) # Color morado/azul oscuro adaptado de la imagen


# ==========================================
# BUCLE AUTOMÁTICO (Desactivado temporalmente en on_ready)
# ==========================================
@tasks.loop(hours=10.0)
async def publicidad_automatica():
    global contador_wikidex, contador_aniversario, toca_wikidex
    
    canal = discord.utils.get(bot.get_all_channels(), name="general")
    if not canal:
        return

    if contador_wikidex >= MAX_REPETICIONES and contador_aniversario >= MAX_REPETICIONES:
        publicidad_automatica.stop()
        return

    if toca_wikidex:
        if contador_wikidex < MAX_REPETICIONES:
            await canal.send(embed=obtener_embed_wikidex())
            contador_wikidex += 1
        toca_wikidex = False
    else:
        if contador_aniversario < MAX_REPETICIONES:
            await canal.send(embed=obtener_embed_aniversario())
            contador_aniversario += 1
        toca_wikidex = True


# ==========================================
# COMANDOS MANUALES
# ==========================================
@bot.command(name="wikidex")
async def wikidex(ctx):
    await ctx.send(embed=obtener_embed_wikidex())

@bot.command(name="aniversario")
async def aniversario(ctx):
    await ctx.send(embed=obtener_embed_aniversario())

@bot.command(name="eventos")
async def eventos(ctx):
    """Envia la tarjeta de Eventos Today con los links en azul en el texto"""
    await ctx.send(embed=obtener_embed_eventos())


# ==========================================
# EVENTO DE ARRANQUE E INICIO DEL BUCLE
# ==========================================
@bot.event
async def on_ready():
    print(f"Bot listo como {bot.user.name}. Modo testeo de comando !eventos activo.")
    
    # Comentado para pausar los envíos automáticos de 10 horas por ahora:
    # if not publicidad_automatica.is_running():
    #     publicidad_automatica.start()

bot.run(os.environ.get("DISCORD_TOKEN"))