import os
import discord
from discord.ext import commands
from datetime import datetime, timezone

# 1. Configuración de permisos lógicos del Bot
intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

# 2. Comando manual !medieva para enviar ÚNICAMENTE el embed compacto fucsia
@bot.command(name="medieva")
async def medieva(ctx):
    # Forzamos a que busque única y exclusivamente el canal llamado "mods"
    canal_objetivo = discord.utils.get(ctx.guild.channels, name="mods")
    destino = canal_objetivo if canal_objetivo else ctx

    # Ruta exacta que coincide con tu carpeta interna de VS Code
    ruta_imagen = os.path.join("images", "image_8dac82.png")
    
    if os.path.exists(ruta_imagen):
        file = discord.File(ruta_imagen, filename="thumbnail.png")
        
        embed = discord.Embed(
            title="✨ Recordatorio de Apoyo",
            description="¡Hola! Recuerda que tenemos un **PayPal** activo para donaciones. Cualquier cantidad es bien apreciada y nos ayuda muchísimo. 💜\n\n👉 https://www.paypal.me/MrBanana450",
            color=14222467,  # Color Fucsia/Púrpura (#d90483)
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_author(name="MedieBot", icon_url="attachment://thumbnail.png")
        embed.set_thumbnail(url="attachment://thumbnail.png")
        
        await destino.send(file=file, embed=embed)
    else:
        # Resguardo en caso de que falle la ruta en el contenedor
        embed_error = discord.Embed(
            title="✨ Recordatorio de Apoyo",
            description="¡Hola! Recuerda que tenemos un **PayPal** activo para donaciones. Cualquier cantidad es bien apreciada y nos ayuda muchísimo. 💜\n\n👉 https://www.paypal.me/MrBanana450",
            color=14222467,
            timestamp=datetime.now(timezone.utc)
        )
        embed_error.set_author(name="MedieBot")
        await destino.send(embed=embed_error)
        print(f"⚠️ No se encontró el archivo en la ruta: {ruta_imagen}")

@bot.event
async def on_ready():
    print(f"🤖 {bot.user.name} listo. Usa !medieva para enviar el embed fucsia a #mods.")

# Tu token original intacto
bot.run(os.environ.get("DISCORD_TOKEN"))