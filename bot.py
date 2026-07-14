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

# Relojes internos en horas para controlar los intervalos
horas_bucle_paleta = 0
horas_bucle_pokeinstinct = 4  # Desfase inicial de 4 horas para que alterne perfectamente con Paleta (Paleta en h0, PokeInstinct en h4, Paleta en h8, PokeInstinct en h12...)
horas_bucle_paypal = 0


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
    # Enlace corregido al PayPal exacto del usuario
    descripcion = (
        "Recuerda que tenemos un PayPal activo para donaciones. "
        f"Cualquier cantidad es bien apreciada y ayuda muchísimo. {emoji_texto}\n\n"
        "👉 [Donar aquí con PayPal](https://www.paypal.me/MrBanana450)"
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
# 3. RELOJ MAESTRO AUTOMÁTICO (ACTIVADO)
# ==========================================
@tasks.loop(hours=1.0)
async def reloj_maestro_publicidad():
    global horas_bucle_paleta, horas_bucle_pokeinstinct, horas_bucle_paypal
    
    canal = discord.utils.get(bot.get_all_channels(), name="general")
    if not canal:
        return

    enviado_paypal_ahora = False
    es_arranque = (horas_bucle_paleta == 0 and horas_bucle_pokeinstinct == 4 and horas_bucle_paypal == 0)

    # 1. COMPROBACIÓN DE PAYPAL (Cada 30 horas o arranque)
    if horas_bucle_paypal >= 30 or es_arranque:
        embed_copia = obtener_embed_paypal()
        embed_copia.set_author(name="MedieBot")
        await canal.send(embed=embed_copia)
        horas_bucle_paypal = 0
        enviado_paypal_ahora = True
        print("[Reloj Maestro] Anuncio de PayPal enviado automáticamente.")

    # 2. COMPROBACIÓN DE PUEBLO PALETA (Cada 8 horas o arranque)
    if horas_bucle_paleta >= 8 or (es_arranque and not enviado_paypal_ahora):
        # Si choca con el envío de PayPal, se pospone 1 hora
        if enviado_paypal_ahora:
            print("[Anti-Choque] Pueblo Paleta coincidió con PayPal. Se pospone 1 hora.")
            horas_bucle_paleta = 7  # Al sumarle 1 al final del loop, quedará en 8 y se evaluará en la siguiente hora
        else:
            await canal.send(embed=obtener_embed_pueblo_paleta())
            horas_bucle_paleta = 0
            print("[Reloj Maestro] Anuncio de Pueblo Paleta enviado automáticamente.")

    # 3. COMPROBACIÓN DE POKEINSTINCT (Cada 8 horas)
    if horas_bucle_pokeinstinct >= 8:
        # Si choca con el envío de PayPal, se pospone 1 hora
        if enviado_paypal_ahora:
            print("[Anti-Choque] PokeInstinct coincidió con PayPal. Se pospone 1 hora.")
            horas_bucle_pokeinstinct = 7  # Al sumarle 1 al final del loop, quedará en 8 y se evaluará en la siguiente hora
        else:
            await canal.send(embed=obtener_embed_poke_instinct())
            horas_bucle_pokeinstinct = 0
            print("[Reloj Maestro] Anuncio de PokeInstinct enviado automáticamente.")

    # Incrementar contadores horarios
    horas_bucle_paleta += 1
    horas_bucle_pokeinstinct += 1
    horas_bucle_paypal += 1


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
    
    if not reloj_maestro_publicidad.is_running():
        reloj_maestro_publicidad.start()
        print("Reloj Maestro de Anuncios activado con intervalos inteligentes (8h / 30h).")

# Encendemos la simulación web para Render
keep_alive()

# Ejecutamos con tu token secreto
bot.run(os.environ.get("DISCORD_TOKEN"))