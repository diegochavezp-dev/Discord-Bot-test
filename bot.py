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

# Variables de control para la automatización
MAX_REPETICIONES = 8
contador_wikidex = 0
contador_aniversario = 0
toca_wikidex = True  # Determina quién empieza. True = WikiDex, False = Aniversario

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


# ==========================================
# BUCLE AUTOMÁTICO (Cada 10 horas de forma alterna)
# ==========================================
@tasks.loop(hours=10.0)
async def publicidad_automatica():
    global contador_wikidex, contador_aniversario, toca_wikidex
    
    # Buscamos el canal llamado "general" automáticamente en el servidor
    canal = discord.utils.get(bot.get_all_channels(), name="general")
    
    if not canal:
        print("Aviso: No encontré ningún canal llamado 'general' todavía.")
        return

    # Verificamos si ya se cumplió la meta global para apagar el bucle por completo
    if contador_wikidex >= MAX_REPETICIONES and contador_aniversario >= MAX_REPETICIONES:
        print("[Auto] Se ha completado la semana de publicidad (8 envíos de cada uno). Deteniendo tarea.")
        publicidad_automatica.stop()
        return

    # CASO A: Toca enviar WikiDex
    if toca_wikidex:
        if contador_wikidex < MAX_REPETICIONES:
            embed = obtener_embed_wikidex()
            await canal.send(embed=embed)
            contador_wikidex += 1
            print(f"[Auto] WikiDex enviado ({contador_wikidex}/{MAX_REPETICIONES})")
        
        # Cambiamos el turno para la siguiente ejecución (dentro de 10 horas)
        toca_wikidex = False

    # CASO B: Toca enviar Aniversario
    else:
        if contador_aniversario < MAX_REPETICIONES:
            embed = obtener_embed_aniversario()
            await canal.send(embed=embed)
            contador_aniversario += 1
            print(f"[Auto] Aniversario Pueblo Paleta enviado ({contador_aniversario}/{MAX_REPETICIONES})")
        
        # Cambiamos el turno para la siguiente ejecución (dentro de 10 horas)
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


# ==========================================
# EVENTO DE ARRANQUE E INICIO DEL BUCLE
# ==========================================
@bot.event
async def on_ready():
    print(f"Bot listo como {bot.user.name}.")
    
    # Iniciamos la tarea programada si no está corriendo
    if not publicidad_automatica.is_running():
        publicidad_automatica.start()
        print("Bucle de publicidad alternada iniciado correctamente (Intervalo: 10 horas).")

bot.run(os.environ.get("DISCORD_TOKEN"))