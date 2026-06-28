import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone

# 1. Configuración de permisos lógicos del Bot
intents = discord.Intents.default()
intents.message_content = True  
intents.reactions = True      
intents.members = True        
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables de control: Envío cada 30 horas durante un mes = 24 veces en total (APAGADO POR AHORA)
MAX_ENVIOS = 24
contador_envios = 0

# Configuración estática de tus IDs reales
ID_MENSAJE_ROLES = 1520818689102970985  

# Mapeo usando los IDs numéricos exactos de tus emojis personalizados
MAPA_ROLES = {
    1514947374647349268: 1520815361979846787,  # KINGS -> Videos
    1520307113430089898: 1520815690003775598,  # LLANTA -> Streams
    1271556869906890837: 1520815766667264120   # pepo -> Torneos
}

# ====================================================================
# RELOJ AUTOMÁTICO DE PAYPAL (COMENTADO / APAGADO TEMPORALMENTE)
# ====================================================================
# @tasks.loop(hours=30.0)
# async def enviar_anuncio_programado():
#     global contador_envios
#     await bot.wait_until_ready()
#     ... (Guardado interno intacto en la papelera para después)
# ====================================================================

# ==========================================
# COMANDO MANUAL PARA LOS ROLES
# ==========================================
@bot.command(name="crearroles")
async def crear_roles(ctx):
    """Manda el embed estructurado de roles usando tus emojis custom"""
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
    
    # Coloca tus emojis personalizados como opciones de reacción abajo
    await mensaje.add_reaction("<:KINGS:1514947374647349268>")
    await mensaje.add_reaction("<:LLANTA:1520307113430089898>")
    await mensaje.add_reaction("<:pepo:1271556869906890837>")

# ==========================================
# ASIGNACIÓN PASIVA POR ID CON DEBUG LOGS
# ==========================================
@bot.event
async def on_raw_reaction_add(payload):
    # Esto imprimirá CUALQUIER reacción en tu consola de Zeabur
    print(f"🔍 [DEBUG] Alguien reaccionó. Mensaje ID: {payload.message_id} | Emoji ID: {payload.emoji.id}")
    
    if payload.message_id != ID_MENSAJE_ROLES:
        print("⚠️ [DEBUG] Reacción ignorada: No pertenece al mensaje de ID_MENSAJE_ROLES.")
        return
        
    guild = bot.get_guild(payload.guild_id)
    if not guild or payload.user_id == bot.user.id:
        return
        
    rol_id = MAPA_ROLES.get(payload.emoji.id)
    print(f"🔍 [DEBUG] Buscando Rol ID en el mapa: {rol_id}")
    
    if rol_id:
        rol = guild.get_role(rol_id)
        miembro = guild.get_member(payload.user_id)
        
        print(f"🔍 [DEBUG] ¿Se encontró el rol en Discord?: {rol is not None}")
        print(f"🔍 [DEBUG] ¿Se encontró al miembro en caché?: {miembro is not None}")
        
        if rol and miembro:
            try:
                await miembro.add_role(rol)
                print(f"✅ Rol asignado exitosamente: {rol.name} a {miembro.name}")
            except Exception as e:
                print(f"❌ ERROR CRÍTICO AL ASIGNAR ROL: {e}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != ID_MENSAJE_ROLES:
        return
        
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
        
    rol_id = MAPA_ROLES.get(payload.emoji.id)
    if rol_id:
        rol = guild.get_role(rol_id)
        miembro = guild.get_member(payload.user_id)
        if rol and miembro:
            try:
                await miembro.remove_role(rol)
                print(f"❌ Rol removido: {rol.name} a {miembro.name}")
            except Exception as e:
                print(f"❌ ERROR AL REMOVER ROL: {e}")

@bot.event
async def on_ready():
    # El reloj de general ya no se arranca aquí, inicia limpio
    print(f"🤖 {bot.user.name} encendido (Modo de prueba de Roles - #general en pausa).")

# Tu token original intacto
bot.run(os.environ.get("DISCORD_TOKEN"))