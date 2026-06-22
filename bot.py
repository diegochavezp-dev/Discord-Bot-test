import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone

# 1. Configuración de permisos lógicos del Bot
intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables de control: Envío cada 30 horas durante un mes = 24 veces en total
MAX_ENVIOS = 24
contador_envios = 0

# 2. Reloj automático: Configurado para ejecutarse exactamente cada 30 horas de frente
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

@bot.event
async def on_ready():
    print(f"🤖 {bot.user.name} encendido. Arrancando reloj automático para #general...")
    if not enviar_anuncio_programado.is_running():
        enviar_anuncio_programado.start()

# Tu token original intacto
bot.run(os.environ.get("DISCORD_TOKEN"))