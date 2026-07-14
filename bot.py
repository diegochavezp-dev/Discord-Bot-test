import os
import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timezone
from flask import Flask
from threading import Thread

# ==========================================
# 0. TRUCO DE TRÁFICO PARA RENDER (Anti-Suspensión)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Bot de Discord en línea y activo 24/7"

def run():
    puerto = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=puerto)

def keep_alive():
    t = Thread(target=run)
    t.start()


# ==========================================
# 1. CONFIGURACIÓN DEL BOT Y VARIABLES
# ==========================================
intents = discord.Intents.default()
intents.message_content = True  
intents.reactions = True      
intents.members = True        
bot = commands.Bot(command_prefix="!", intents=intents)

# Relojes internos (Desactivados por ahora)
horas_bucle_10h = 0
horas_bucle_30h = 0


# ==========================================
# 2. DISEÑO DE LOS EMBEDS
# ==========================================
def obtener_embed_pueblo_paleta():
    emoji_texto = "<:quagwin:1271553155108442125>"
    descripcion = (
        "¿Buscas un lugar donde hablar de Pokémon, participar en torneos y conocer gente con la misma afición?\n\n"
        "En **Pueblo Paleta** organizamos eventos, competiciones y actividades para mantener la comunidad siempre activa. "
        "Tanto si vienes a competir como a pasar un buen rato, aquí encontrarás tu sitio.\n\n"
        f"¡Únete a Pueblo Paleta y forma parte de nuestra bonita comunidad! {emoji_texto}\n\n"
        "Discord: https://discord.gg/vbpSZEevtv"
    )
    return discord.Embed(description=descripcion, color=16515241)

def obtener_embed_paypal():
    emoji_texto = "<:dechill:1271555851227889716>"
    descripcion = (
        "Recuerda que tenemos un PayPal activo para donaciones. "
        f"Cualquier cantidad es bien apreciada y ayuda muchísimo. {emoji_texto}\n\n"
        "👉 [Donar aquí con PayPal](https://www.paypal.com)" # <-- Cambia por tu link real de PayPal
    )
    embed = discord.Embed(
        description=descripcion,
        color=10181046,
        timestamp=datetime.now(timezone.utc)
    )
    return embed

def obtener_embed_poke_instinct():
    emoji_texto = "⚔️"
    descripcion = (
        "¿Solo entras al Showdown para jugar ladder? ¿Buscas algo más que una simple victoria?\n\n"
        "En **PokeInstinct** encontrarás una comunidad donde el competitivo cobra vida. "
        "Participa en torneos, aprende nuevas estrategias, reta a otros entrenadores, "
        "forma equipos para competiciones y mejora junto a jugadores de todos los niveles.\n\n"
        "Ya sea que quieras dar tus primeros pasos en el competitivo o convertirte en un rival de alto nivel, "
        "aquí siempre habrá alguien dispuesto a ayudarte... o a intentar derrotarte.\n\n"
        f"¡Únete a PokeInstinct y demuestra que tienes lo necesario para convertirte en un verdadero campeón! {emoji_texto}\n\n"
        "Discord: https://discord.gg/gf34vySGrb"
    )
    return discord.Embed(description=descripcion, color=15087942)


# ==========================================
# 3. RELOJ MAESTRO AUTOMÁTICO (APAGADO)
# ==========================================
@tasks.loop(hours=1.0)
async def reloj_maestro_publicidad():
    global horas_bucle_10h, horas_bucle_30h
    
    canal = discord.utils.get(bot.get_all_channels(), name="general")
    if not canal:
        return

    enviado_en_esta_hora = False
    es_arranque = (horas_bucle_10h == 0 and horas_bucle_30h == 0)

    if horas_bucle_10h >= 10 or es_arranque:
        await canal.send(embed=obtener_embed_pueblo_paleta())
        horas_bucle_10h = 0
        enviado_en_esta_hora = True

    if horas_bucle_30h >= 30 or es_arranque:
        if enviado_en_esta_hora:
            pass
        else:
            embed_copia = obtener_embed_paypal()
            embed_copia.set_author(name="MedieBot")
            await canal.send(embed=embed_copia)
            horas_bucle_30h = 0

    horas_bucle_10h += 1
    horas_bucle_30h += 1


# ==========================================
# 4. COMANDOS MANUALES
# ==========================================
@bot.command(name="pueblopaleta")
async def pueblopaleta(commands_ctx):
    """Manda el embed de Pueblo Paleta manualmente"""
    await commands_ctx.send(embed=obtener_embed_pueblo_paleta())

@bot.command(name="paypal")
async def paypal(commands_ctx):
    """Manda el embed de PayPal limpio sin duplicar el avatar"""
    embed = obtener_embed_paypal()
    embed.set_author(name="MedieBot")
    await commands_ctx.send(embed=embed)

@bot.command(name="pokeinstinct")
async def pokeinstinct(commands_ctx):
    """Manda el embed de PokeInstinct manualmente"""
    await commands_ctx.send(embed=obtener_embed_poke_instinct())


# ==========================================
# 5. ARRANQUE DEL BOT
# ==========================================
@bot.event
async def on_ready():
    print(f"Bot unificado listo como {bot.user.name}.")
    print("Autoenvíos apagados. El Reloj Maestro no se iniciará.")
    # El reloj automático está comentado para que no se ejecute:
    # if not reloj_maestro_publicidad.is_running():
    #     reloj_maestro_publicidad.start()

# Encendemos la simulación web para Render
keep_alive()

# Ejecutamos con tu token secreto
bot.run(os.environ.get("DISCORD_TOKEN"))