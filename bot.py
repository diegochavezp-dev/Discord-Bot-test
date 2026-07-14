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

# Relojes internos para controlar el envío automático (en horas)
horas_bucle_10h = 0
horas_bucle_30h = 0


# ==========================================
# 2. DISEÑO DE LOS EMBEDS (Pueblo Paleta y PayPal)
# ==========================================
def obtener_embed_pueblo_paleta():
    emoji_texto = "<:quagwin:1271553155108442125>"
    # Se añade el salto de línea (\n\n) después de "afición?" para mejorar la visualización
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
    # Descripción en negrita para máxima legibilidad
    descripcion_en_negrita = (
        "**Recuerda que tenemos un PayPal activo para donaciones. "
        f"Cualquier cantidad es bien apreciada y ayuda muchísimo.** {emoji_texto}"
    )
    embed = discord.Embed(
        description=descripcion_en_negrita,
        color=10181046,
        timestamp=datetime.now(timezone.utc)
    )
    return embed


# ==========================================
# 3. RELOJ MAESTRO AUTOMÁTICO (ACTIVADO)
# ==========================================
@tasks.loop(hours=1.0)
async def reloj_maestro_publicidad():
    global horas_bucle_10h, horas_bucle_30h
    
    canal = discord.utils.get(bot.get_all_channels(), name="general")
    if not canal:
        return

    enviado_en_esta_hora = False
    es_arranque = (horas_bucle_10h == 0 and horas_bucle_30h == 0)

    # Comprobación de Pueblo Paleta (Cada 10 horas)
    if horas_bucle_10h >= 10 or es_arranque:
        await canal.send(embed=obtener_embed_pueblo_paleta())
        horas_bucle_10h = 0
        enviado_en_esta_hora = True
        print("[Reloj Maestro] Anuncio de Pueblo Paleta enviado automáticamente.")

    # Comprobación de PayPal (Cada 30 horas)
    if horas_bucle_30h >= 30 or es_arranque:
        if enviado_en_esta_hora:
            print("[Anti-Choque] PayPal iba a coincidir con Pueblo Paleta. Se pospone 1 hora.")
        else:
            embed_copia = obtener_embed_paypal()
            embed_copia.set_author(name="MedieBot")
            await canal.send(embed=embed_copia)
            horas_bucle_30h = 0
            print("[Reloj Maestro] Anuncio de PayPal enviado automáticamente.")

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


# ==========================================
# 5. ARRANQUE DEL BOT
# ==========================================
@bot.event
async def on_ready():
    print(f"Bot unificado listo como {bot.user.name}.")
    
    if not reloj_maestro_publicidad.is_running():
        reloj_maestro_publicidad.start()
        print("Reloj Maestro de Anuncios activado en segundo plano de forma indefinida.")

# Encendemos la simulación web para Render
keep_alive()

# Ejecutamos con tu token secreto desde las variables de entorno
bot.run(os.environ.get("DISCORD_TOKEN"))