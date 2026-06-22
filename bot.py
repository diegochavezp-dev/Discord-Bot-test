import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone

# 1. Configuración de permisos lógicos del Bot
intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables de control: 3 días * 3 envíos por día = 9 veces en total
MAX_ENVIOS = 9
contador_envios = 0

# 2. Creación de los Botones Físicos Rectangulares
class RedesSocialesView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            label="Síguenos en X / Twitter", 
            url="https://x.com/MetapodPresi", 
            style=discord.ButtonStyle.link
        ))
        self.add_item(discord.ui.Button(
            label="Suscríbete en Facebook", 
            url="https://www.facebook.com/Metapodpresidente/?locale=es_LA", 
            style=discord.ButtonStyle.link
        ))

# 3. Reloj automático: Ejecuta esta función exactamente cada 8 horas
@tasks.loop(hours=8.0)
async def enviar_anuncio_programado():
    global contador_envios
    await bot.wait_until_ready()
    
    for guild in bot.guilds:
        # CORREGIDO: Ahora el bucle automático sí busca "seccion1"
        canal_seccion = discord.utils.get(guild.channels, name="seccion1")
        
        if canal_seccion and contador_envios < MAX_ENVIOS:
            mencion_canal = canal_seccion.mention
            
            embed = discord.Embed(
                title="Bienvenido a Medieva",
                description=f"**Banana**\n\ndame la chamba en {mencion_canal}\n\n*Test*",
                color=5793266,
                timestamp=datetime.now(timezone.utc)
            )
            embed.set_thumbnail(url="https://i.ebayimg.com/images/g/BOIAAOSw-0xYiZYC/s-l1200.jpg")
            embed.set_image(url="https://www.pokemon.com/static-assets/content-assets/cms2/img/video-games/_tiles/strategy/go/mega-beedrill/pokemon-go-169.png")
            
            await canal_seccion.send(embed=embed, view=RedesSocialesView())
            
            contador_envios += 1
            print(f" Anuncio enviado automáticamente ({contador_envios}/{MAX_ENVIOS})")
            
    if contador_envios >= MAX_ENVIOS:
        print(" Bucle terminado (3 días cumplidos). Deteniendo tarea.")
        enviar_anuncio_programado.stop()

@bot.event
async def on_ready():
    print(f"🤖 Bot encendido y conectado con éxito como {bot.user}!")
    if not enviar_anuncio_programado.is_running():
        enviar_anuncio_programado.start()

# Comando manual por si quieres probarlo escribiendo !medieva
@bot.command(name="medieva")
async def medieva(ctx):
    canal_seccion = discord.utils.get(ctx.guild.channels, name="seccion1")
    mencion_canal = canal_seccion.mention if canal_seccion else "#seccion1"
    
    embed = discord.Embed(
        title="Bienvenido a Medieva",
        description=f"**Banana**\n\ndame la chamba en {mencion_canal}",
        color=5793266,
        timestamp=datetime.now(timezone.utc)
    )
    embed.set_thumbnail(url="https://i.ebayimg.com/images/g/BOIAAOSw-0xYiZYC/s-l1200.jpg")
    embed.set_image(url="https://www.pokemon.com/static-assets/content-assets/cms2/img/video-games/_tiles/strategy/go/mega-beedrill/pokemon-go-169.png")
    
    # Asegura que el comando manual también mande el mensaje a #seccion1
    destino = canal_seccion if canal_seccion else ctx
    await destino.send(embed=embed, view=RedesSocialesView())

# Tu token original intacto
bot.run(os.environ.get("DISCORD_TOKEN"))