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

# Reloj interno en horas
horas_bucle_8h = 0

# Control global para activar/desactivar el bucle automático (Inicia desactivado para pruebas)
anuncios_automaticos_activos = False 

# Interruptor para alternar los dos anuncios restantes
# True = Toca PokeInstinct | False = Toca Torneo Mundial
toca_pokeinstinct = True


# ==========================================
# 2. DISEÑO DE LOS EMBEDS Y CONTENIDO
# ==========================================
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

def obtener_embed_torneo_mundial():
    descripcion = (
        "Este mes nos ponemos en modo **Mundial**. ⚽✨\n\n"
        "🇪🇸🇲🇽🇦🇷🇯🇵🇧🇷... **elige los colores de tu bandera**, crea un equipo "
        "inspirado en tu país y demuestra quién merece levantar la copa.\n\n"
        "Hay casteos y premios, para motivar todo lo que se pueda y poder "
        "revivir ESE momento siempre que quieras, forma parte de la historia del canal 🩷🔥\n\n"
        "📅 **Domingo 26 de julio**\n"
        "🕗 **20:00 (hora española)**\n\n"
        "¿Representarás a tu nación hasta lo más alto del podio? 🌎🔥\n\n"
        "📋 Toda la información e inscripciones aquí:"
    )
    embed = discord.Embed(
        title="🌍🏆 ¡Llega la Pokémon XIII Tournament #10! 🏆🌍",
        description=descripcion,
        color=4672324  # Color oscuro integrado al chat (RGB 47, 49, 54 aproximado)
    )
    embed.set_footer(text="¡Nos vemos en el campo de batalla! ⚔️")
    return embed

# Link externo para forzar la vista previa/tarjeta de Battlefy en Discord
link_torneo_battlefy = "https://battlefy.com/imperio-impar/pok%C3%A9mon-xiii-tournament-10/6a4c92d3738cf50021bbcf39/info"


# ==========================================
# 3. RELOJ MAESTRO AUTOMÁTICO
# ==========================================
@tasks.loop(hours=1.0)
async def reloj_maestro_publicidad():
    global horas_bucle_8h, toca_pokeinstinct, anuncios_automaticos_activos
    
    # Si el interruptor global está en False, no procesa el envío automático
    if not anuncios_automaticos_activos:
        return

    canal = discord.utils.get(bot.get_all_channels(), name="general")
    if not canal:
        return

    es_arranque = (horas_bucle_8h == 0)

    # COMPROBACIÓN DEL ANUNCIO DE 8 HORAS
    if horas_bucle_8h >= 8 or es_arranque:
        if toca_pokeinstinct:
            await canal.send(embed=obtener_embed_poke_instinct())
            print("[Reloj Maestro] Turno de PokeInstinct enviado automáticamente.")
            toca_pokeinstinct = False  # Siguiente turno será Torneo
        else:
            await canal.send(embed=obtener_embed_torneo_mundial())
            await canal.send(link_torneo_battlefy)
            print("[Reloj Maestro] Turno de Torneo Mundial enviado automáticamente con su link.")
            toca_pokeinstinct = True  # Siguiente turno será PokeInstinct
            
        horas_bucle_8h = 0

    # Incrementar contador horario
    horas_bucle_8h += 1


# ==========================================
# 4. COMANDOS MANUALES PARA PRUEBAS
# ==========================================
@bot.command(name="test_instinct")
async def test_instinct(commands_ctx):
    """Manda el embed de PokeInstinct manualmente para pruebas"""
    await commands_ctx.send(embed=obtener_embed_poke_instinct())

@bot.command(name="test_torneo")
async def test_torneo(commands_ctx):
    """Manda el embed del Torneo y el link externo para verificar el diseño visual exacto"""
    await commands_ctx.send(embed=obtener_embed_torneo_mundial())
    await commands_ctx.send(link_torneo_battlefy)

@bot.command(name="toggle_ads")
async def toggle_ads(commands_ctx, estado: bool):
    """Permite encender (True) o apagar (False) el envío automático desde Discord"""
    global anuncios_automaticos_activos
    anuncios_automaticos_activos = estado
    status = "ACTIVADOS" if estado else "DESACTIVADOS"
    await commands_ctx.send(f"📢 Los anuncios automáticos ahora están: **{status}**")


# ==========================================
# 5. ARRANQUE DEL BOT
# ==========================================
@bot.event
async def on_ready():
    print(f"Bot unificado listo como {bot.user.name}.")
    
    if not reloj_maestro_publicidad.is_running():
        reloj_maestro_publicidad.start()
        print("Reloj Maestro inicializado (Modo manual activo por defecto. Usa !toggle_ads true para automatizar).")

# Encendemos la simulación web para Render
keep_alive()

# Ejecutamos con tu token secreto
bot.run(os.environ.get("DISCORD_TOKEN"))