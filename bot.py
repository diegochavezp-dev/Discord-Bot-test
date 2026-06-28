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

# Configuracion estatica actualizada con tu ID de mensaje real
ID_MENSAJE_ROLES = 1520827606474166273  

# Mapeo usando los nuevos IDs numericos exactos de tus emojis personalizados
MAPA_ROLES = {
    1271553118454153268: 1520815361979846787,  # medo -> Videos
    1271553135718039633: 1520815690003775598,  # hail -> Streams
    1271557610272854119: 1520815766667264120   # huh -> Torneos
}

# ==========================================
# COMANDO MANUAL PARA LOS ROLES
# ==========================================
@bot.command(name="crearroles")
async def crear_roles(ctx):
    ruta_imagen = os.path.join("images", "jj.webp")
    
    descripcion = (
        f"<:medo:1271553118454153268> Videos\n"
        f"<:hail:1271553135718039633> Streams\n"
        f"<:huh:1271557610272854119> Torneos/Eventos"
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
    
    await mensaje.add_reaction("<:medo:1271553118454153268>")
    await mensaje.add_reaction("<:hail:1271553135718039633>")
    await mensaje.add_reaction("<:huh:1271557610272854119>")

# ==========================================
# ASIGNACION PASIVA POR REACCIONES (LIMPIO)
# ==========================================
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != ID_MENSAJE_ROLES:
        return
        
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        try:
            guild = await bot.fetch_guild(payload.guild_id)
        except Exception:
            return
            
    if payload.user_id == bot.user.id:
        return
        
    rol_id = MAPA_ROLES.get(payload.emoji.id)
    if rol_id:
        rol = guild.get_role(rol_id)
        miembro = guild.get_member(payload.user_id)
        if not miembro:
            try:
                miembro = await guild.fetch_member(payload.user_id)
            except Exception:
                return
                
        if rol and miembro:
            try:
                await miembro.add_role(rol)
            except Exception:
                pass

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != ID_MENSAJE_ROLES:
        return
        
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        try:
            guild = await bot.fetch_guild(payload.guild_id)
        except Exception:
            return
        
    rol_id = MAPA_ROLES.get(payload.emoji.id)
    if rol_id:
        rol = guild.get_role(rol_id)
        miembro = guild.get_member(payload.user_id)
        if not miembro:
            try:
                miembro = await guild.fetch_member(payload.user_id)
            except Exception:
                return
                
        if rol and miembro:
            try:
                await miembro.remove_role(rol)
            except Exception:
                pass

@bot.event
async def on_ready():
    print("Bot encendido correctamente y escuchando eventos pasivos.")

bot.run(os.environ.get("DISCORD_TOKEN"))