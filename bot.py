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

# Variables de control de repeticiones (Máximo 8 de cada uno)
MAX_REPETICIONES = 8
contador_wikidex = 0
contador_aniversario = 0
contador_eventos = 0

# Relojes internos en horas (Llevan la cuenta de cuántas horas han pasado)
horas_bucle_10h = 0
horas_bucle_7h = 0
toca_wikidex = True # Alternador para el grupo de 10 horas

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
        "**¿Mucho vacío con los torneos? ¿quieres algo más allá de presionar botones contra el oponente? "
        "¿Cansado de scouting, haxing y schedule? ¡[Eventos](<https://play.pokemonshowdown.com/eventos>) es lo que necesitas! "
        "La sala que da eventos y torneos exclusivos por dinero, CAVY, recompensas como tarjetas de steam o la sencilla "
        "gloria de vencer a un tryhard y alimentar tu ego... Podrás hacer tus propios mons en el SSB, vencer desafíos en "
        "equipo en el CAMP, poner tu inteligencia a prueba en la Torre y tener acceso privilegiado a torneos para eventinos. "
        "La comunidad te espera con los brazos abiertos, ¡[Eventos](<https://play.pokemonshowdown.com/eventos>) espera tu desafío!**\n\n"
        "**¡Unete al Servidor NO oficial de Eventos, [Eventos Today](https://discord.gg/JTNPehs3c) donde podrás interactuar, "
        "shitpostear y divertirte con nosotros!**\n\n"
        "Discord: https://discord.gg/JTNPehs3c"
    )
    return discord.Embed(description=descripcion, color=5641372)


# ==========================================
# RELEJ MAESTRO ANTI-CHOQUES (Revisa cada 1 hora)
# ==========================================
@tasks.loop(hours=1.0)
async def reloj_maestro_publicidad():
    global contador_wikidex, contador_aniversario, contador_eventos
    global horas_bucle_10h, horas_bucle_7h, toca_wikidex
    
    canal = discord.utils.get(bot.get_all_channels(), name="general")
    if not canal:
        return

    # Si todo ya se mandó 8 veces, apagamos el reloj definitivo
    if contador_wikidex >= MAX_REPETICIONES and contador_aniversario >= MAX_REPETICIONES and contador_eventos >= MAX_REPETICIONES:
        print("[Reloj Maestro] Toda la publicidad completada. Apagando sistema.")
        reloj_maestro_publicidad.stop()
        return

    enviado_en_esta_hora = False

    # 1. COMPROBACIÓN GRUPO 10 HORAS (WikiDex / Aniversario)
    if horas_bucle_10h >= 10 or (contador_wikidex == 0 and contador_aniversario == 0 and horas_bucle_10h == 0):
        if toca_wikidex and contador_wikidex < MAX_REPETICIONES:
            await canal.send(embed=obtener_embed_wikidex())
            contador_wikidex += 1
            horas_bucle_10h = 0
            toca_wikidex = False
            enviado_en_esta_hora = True
            print(f"[Reloj Maestro] WikiDex enviado ({contador_wikidex}/{MAX_REPETICIONES})")
        elif not toca_wikidex and contador_aniversario < MAX_REPETICIONES:
            await canal.send(embed=obtener_embed_aniversario())
            contador_aniversario += 1
            horas_bucle_10h = 0
            toca_wikidex = True
            enviado_en_esta_hora = True
            print(f"[Reloj Maestro] Aniversario enviado ({contador_aniversario}/{MAX_REPETICIONES})")

    # 2. COMPROBACIÓN GRUPO 7 HORAS (Eventos Today)
    # Si le toca salir a Eventos pero ya se envió un mensaje en esta hora, lo aplazamos 1 hora más para evitar el choque
    if horas_bucle_7h >= 7 or (contador_eventos == 0 and horas_bucle_7h == 0):
        if contador_eventos < MAX_REPETICIONES:
            if enviado_en_esta_hora:
                print("[Anti-Choque] Eventos iba a coincidir. Se pospone 1 hora automáticamente.")
                # No reiniciamos el contador de horas_bucle_7h, así volverá a intentarlo en la siguiente hora
            else:
                await canal.send(embed=obtener_embed_eventos())
                contador_eventos += 1
                horas_bucle_7h = 0
                print(f"[Reloj Maestro] Eventos enviado ({contador_eventos}/{MAX_REPETICIONES})")

    # Sumamos una hora a los contadores de tiempo para el siguiente ciclo
    horas_bucle_10h += 1
    horas_bucle_7h += 1


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
    await ctx.send(embed=obtener_embed_eventos())


# ==========================================
# EVENTO DE ARRANQUE E INICIO DE TEMPORIZADOR
# ==========================================
@bot.event
async def on_ready():
    print(f"Bot listo como {bot.user.name}.")
    
    if not reloj_maestro_publicidad.is_running():
        reloj_maestro_publicidad.start()
        print("Reloj Maestro Inteligente (Anti-Choques) activado.")

bot.run(os.environ.get("DISCORD_TOKEN"))