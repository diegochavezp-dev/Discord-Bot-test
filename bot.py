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

# 2. Reloj automático: Ejecuta esta función exactamente cada 8 horas de frente
@tasks.loop(hours=8.0)
async def enviar_anuncio_programado():
    global contador_envios
    await bot.wait_until_ready()
    
    # El código interno exacto que obtuviste del chat
    emoji_texto = "<:dechill:1271555851227889716>"
    
    for guild in bot.guilds:
        # Busca automáticamente el canal llamado "mods" en cada servidor
        canal_objetivo = discord.utils.get(guild.channels, name="mods")
        
        if canal_objetivo and contador_envios < MAX_ENVIOS:
            # Apunta de forma exacta a tu archivo local en la carpeta images
            ruta_imagen = os.path.join("images", "jj.webp")
            
            if os.path.exists(ruta_imagen):
                file = discord.File(ruta_imagen, filename="avatar.webp")
                
                # Embed limpio usando tu emoji verificado al final
                embed = discord.Embed(
                    description=f"Recuerda que tenemos un **PayPal** activo para donaciones. Cualquier cantidad es bien apreciada y ayuda muchísimo. {emoji_texto}\n\n👉 [Donar aquí con PayPal](https://www.paypal.me/MrBanana450)",
                    color=10181046,  # Color púrpura exacto del rol de MrBanana45
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
            print(f" Anuncio enviado automáticamente ({contador_envios}/{MAX_ENVIOS})")
            
    if contador_envios >= MAX_ENVIOS:
        print(" Bucle terminado (3 días cumplidos). Deteniendo tarea.")
        enviar_anuncio_programado.stop()

@bot.event
async def on_ready():
    print(f"🤖 {bot.user.name} encendido. Arrancando reloj automático para #mods...")
    if not enviar_anuncio_programado.is_running():
        enviar_anuncio_programado.start()

# Tu token original intacto
bot.run(os.environ.get("DISCORD_TOKEN"))