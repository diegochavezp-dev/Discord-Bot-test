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

# Configuracion estatica de tus IDs reales
ID_MENSAJE_ROLES = 1520818689102970985  

# Mapeo usando los IDs numericos exactos de tus emojis personalizados
MAPA_ROLES = {
    1514947374647349268: 1520815361979846787,  # KINGS -> Videos
    1520307113430089898: 1520815690003775598,  # LLANTA -> Streams
    1271556869906890837: 1520815766667264120   # pepo -> Torneos
}

# ==========================================
# COMANDO MANUAL PARA LOS ROLES
# ==========================================
@bot.command(name="crearroles")
async def crear_roles(ctx):
    ruta_imagen = os.path.join("images", "jj.webp")
    
    descripcion = (
        f"<:KINGS:1514947374647349268> Videos\n"
        f"<:LLANTA:1520307113430089898> Streams\n"
        f"<:pepo:1271556869906890837> Torneos/Eventos"
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
    
    await mensaje.add_reaction("<:KINGS:1514947374647349268>")
    await mensaje.add_reaction("<:LLANTA:1520307113430089898>")
    await mensaje.add_reaction("<:pepo:1271556869906890837>")

# ==========================================
# ASIGNACION PASIVA POR ID CON DEBUG SEGURO
# ==========================================
@bot.event
async def on_raw_reaction_add(payload):
    # Debug limpio sin caracteres extraños para no congelar la consola
    print(f"[DEBUG] Reaccion detectada. MSG ID: {payload.message_id} | Emoji ID: {payload.emoji.id}")
    
    if payload.message_id != ID_MENSAJE_ROLES:
        return
        
    # Forzamos la busqueda en la API si no esta cargado en la cache de Zeabur
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
        
        # Estrategia de respaldo: Si el miembro devuelve None, lo descargamos directo de Discord
        miembro = guild.get_member(payload.user_id)
        if not miembro:
            try:
                miembro = await guild.fetch_member(payload.user_id)
            except Exception as e:
                print(f"[DEBUG] Error al buscar miembro en Discord: {e}")
                return
                
        if rol and miembro:
            try:
                await miembro.add_role(rol)
                print(f"[OK] Rol asignado correctamente")
            except Exception as e:
                print(f"[ERR] No se pudo asignar por permisos: {e}")

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
                print(f"[OK] Rol removido correctamente")
            except Exception as e:
                print(f"[ERR] No se pudo remover: {e}")

@bot.event
async def on_ready():
    print("Bot encendido correctamente y escuchando eventos pasivos.")

bot.run(os.environ.get("DISCORD_TOKEN"))