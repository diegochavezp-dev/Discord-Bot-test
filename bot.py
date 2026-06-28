import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone

# 1. Configuración de permisos lógicos del Bot
intents = discord.Intents.default()
intents.message_content = True  
intents.reactions = True      # Requerido para capturar las reacciones pasivas
intents.members = True        # Requerido para poder gestionar y dar roles a usuarios
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables de control: Envío cada 30 horas durante un mes = 24 veces en total
MAX_ENVIOS = 24
contador_envios = 0

# 👇 CONFIGURACIÓN: Reemplaza el 0 de abajo con el ID del mensaje tras usar !crearroles por primera vez
ID_MENSAJE_ROLES = 1520818689102970985  

ID_ROL_VIDEOS = 1520815361979846787
ID_ROL_STREAMS = 1520815690003775598
ID_ROL_TORNEOS = 1520815766667264120

# Diccionario mapeando tus emojis con tus IDs de roles reales suministrados
MAPA_ROLES = {
    "🎥": ID_ROL_VIDEOS,
    "🎮": ID_ROL_STREAMS,
    "🏆": ID_ROL_TORNEOS
}

# 2. Reloj automático: Configurado para ejecutarse exactamente cada 30 horas de frente (INTACTO)
@tasks.loop(hours=30.0)
async def enviar_anuncio_programado():
    global contador_envios
    await bot.wait_until_ready()
    
    # Tu emoji verificado del chat
    emoji_texto = "<:dechill:1271555851227889716>"
    
    for guild in bot.guilds:
        # Busca el canal llamado "general" (solo lo enviará en el servidor que lo tenga)
        canal_objetivo = discord.utils.get(guild.channels, name="general")
        
        if canal_objetivo and contador_envios < MAX_ENVIOS:
            ruta_imagen = os.path.join("images", "jj.webp")
            
            if os.path.exists(ruta_imagen):
                file = discord.File(ruta_imagen, filename="avatar.webp")
                
                # Embed compacto con el color púrpura de su rol
                embed = discord.Embed(
                    description=f"Recuerda que tenemos un **PayPal** activo para donaciones. Cualquier cantidad es bien apreciada y ayuda muchísimo. {emoji_texto}\n\n👉 [Donar aquí con PayPal](https://www.paypal.me/MrBanana450)",
                    color=10181046,
                    timestamp=datetime.now(timezone.utc)
                )
                embed.set_author(name="MedieBot", icon_url="attachment://avatar.webp")
                
                await canal_objetivo.send(file=file, embed=embed)
            else:
                # Resguardo por si la imagen jj.webp no se encuentra en el contenedor
                embed_error = discord.Embed(
                    description=f"Recuerda que tenemos un **PayPal** activo para donaciones. Cualquier cantidad es bien apreciada y ayuda muchísimo. {emoji_texto}\n\n👉 [Donar aquí con PayPal](https://www.paypal.me/MrBanana450)",
                    color=10181046,
                    timestamp=datetime.now(timezone.utc)
                )
                embed_error.set_author(name="MedieBot")
                await canal_objetivo.send(embed=embed_error)
                print(f"⚠️ No se encontró la imagen en: {ruta_imagen}")
            
            contador_envios += 1
            print(f" Anuncio enviado automáticamente a #general ({contador_envios}/{MAX_ENVIOS})")
            
    if contador_envios >= MAX_ENVIOS:
        print(" Bucle terminado (1 mes cumplido). Deteniendo tarea.")
        enviar_anuncio_programado.stop()

# ====================================================================
# NUEVA FUNCIÓN: COMANDO DE ROLES POR REACCIÓN (ACTIVA EN DONDE SEA)
# ====================================================================
@bot.command(name="crearroles")
async def crear_roles(ctx):
    """Manda el embed estructurado de roles en el canal donde se ejecute el comando"""
    ruta_imagen = os.path.join("images", "jj.webp")
    emoji_video = "🎥"
    emoji_stream = "🎮"
    emoji_torneo = "🏆"
    
    descripcion = (
        f"{emoji_video} Videos\n"
        f"{emoji_stream} Streams\n"
        f"{emoji_torneo} Torneos/Eventos"
    )
    
    if os.path.exists(ruta_imagen):
        file = discord.File(ruta_imagen, filename="avatar.webp")
        embed = discord.Embed(description=descripcion, color=10181046, timestamp=datetime.now(timezone.utc))
        embed.set_author(name="MedieBot", icon_url="attachment://avatar.webp")
        mensaje = await ctx.send(file=file, embed=embed)
    else:
        embed_error = discord.Embed(description=descripcion, color=10181046, timestamp=datetime.now(timezone.utc))
        embed_error.set_author(name="MedieBot")
        mensaje = await ctx.send(embed=embed_error)
    
    # Agrega de inmediato las reacciones base abajo del embed
    await mensaje.add_reaction(emoji_video)
    await mensaje.add_reaction(emoji_stream)
    await mensaje.add_reaction(emoji_torneo)
    
    print(f"📢 Mensaje de roles enviado en #{ctx.channel.name}. ID de Mensaje: {mensaje.id}")

@bot.event
async def on_raw_reaction_add(payload):
    """Escucha pasiva: Asigna el rol correspondiente cuando un usuario reacciona"""
    if payload.message_id != ID_MENSAJE_ROLES:
        return
        
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
        
    rol_id = MAPA_ROLES.get(payload.emoji.name)
    if rol_id:
        rol = guild.get_role(rol_id)
        miembro = guild.get_member(payload.user_id)
        if rol and miembro and not miembro.bot:
            await miembro.add_role(rol)
            print(f"✅ Rol asignado de forma exitosa: {rol.name} a {miembro.name}")

@bot.event
async def on_raw_reaction_remove(payload):
    """Escucha pasiva: Remueve el rol correspondiente cuando un usuario quita su reacción"""
    if payload.message_id != ID_MENSAJE_ROLES:
        return
        
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
        
    rol_id = MAPA_ROLES.get(payload.emoji.name)
    if rol_id:
        rol = guild.get_role(rol_id)
        miembro = guild.get_member(payload.user_id)
        if rol and miembro:
            await miembro.remove_role(rol)
            print(f"❌ Rol removido de forma exitosa: {rol.name} a {miembro.name}")

# ====================================================================

@bot.event
async def on_ready():
    print(f"🤖 {bot.user.name} encendido. Arrancando reloj automático para #general...")
    if not enviar_anuncio_programado.is_running():
        enviar_anuncio_programado.start()

# Tu token original intacto
bot.run(os.environ.get("DISCORD_TOKEN"))