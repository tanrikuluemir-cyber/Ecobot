
import discord
import random
import os
import requests
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')


# Geri donusum rehberi
@bot.command()
async def geri_donusum(ctx):
    await ctx.send(
        "Geri donusturulebilir malzemeler:\n"
        "Cam, kagit, plastik ve metal.\n"
        "Geri donusum cevreyi korur!"
    )


# Cevre tavsiyesi
@bot.command()
async def tavsiye(ctx):
    tavsiyeler = [
        "Plastik sise yerine matara kullan!",
        "Alisveris yaparken bez canta kullan!",
        "Kullanmadigin isiklari kapat!",
        "Atiklarini geri donustur!",
        "Suyu bosa harcama!"
    ]
    await ctx.send("Cevre tavsiyesi: " + random.choice(tavsiyeler))


# Cevre gorevi
@bot.command()
async def gorev(ctx):
    gorevler = [
        "Bugun plastik sise kullanma!",
        "Bugun suyu bosa harcama!",
        "Bugun bez canta kullan!",
        "Bugun kagitlari geri donustur!"
    ]
    await ctx.send("Gunun cevre gorevi: " + random.choice(gorevler))


@bot.command()
async def resim(ctx):
    resimler = [
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800",
        "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800"
        "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=800",
        "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=800",
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
        "https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=800",
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800"

    ]

    resim_url = random.choice(resimler)

    embed = discord.Embed(
        title="Dogayi koruyalim!",
        description="Geri donusum yap ve cevreyi koru!",
        color=discord.Color.green()
    )

    embed.set_image(url=resim_url)

    await ctx.send(embed=embed)



@bot.command()
async def bilgi(ctx):
    bilgiler = [
        {
            "baslik": "Agaclarin onemi",
            "aciklama": "Agaclar karbondioksiti emer ve canlilar icin oksijen uretilmesine yardim eder.",
            "resim": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800"
        },
        {
            "baslik": "Geri donusum",
            "aciklama": "Kagit, cam, plastik ve metal gibi bircok malzeme geri donusturulebilir.",
            "resim": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800"
        },
        {
            "baslik": "Su tasarrufu",
            "aciklama": "Dislerini fircalarken muslugu kapatmak su tasarrufu yapmaya yardim eder.",
            "resim": "https://images.unsplash.com/photo-1437482078695-73f5ca6c96e2?w=800"
        },
        {
            "baslik": "Ormanlari koruyalim",
            "aciklama": "Ormanlar hayvanlara yuva olur ve doganin dengesini korumaya yardim eder.",
            "resim": "https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=800"
        }
    ]

    bilgi = random.choice(bilgiler)

    embed = discord.Embed(
        title="🌍 " + bilgi["baslik"],
        description=bilgi["aciklama"],
        color=discord.Color.green()
    )

    embed.set_image(url=bilgi["resim"])

    await ctx.send(embed=embed)







@bot.command()
async def quiz(ctx):
    sorular = [
        {
            "soru": "Kagit hangi kutuya atilir?",
            "cevaplar": ["Mavi", "Yesil", "Sari"],
            "dogru": 0,
            "resim": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800"
        },
        {
            "soru": "Dislerini fircalarken ne yapmalisin?",
            "cevaplar": [
                "Suyu acik birak",
                "Muslugu kapat",
                "Daha cok su kullan"
            ],
            "dogru": 1,
            "resim": "https://images.unsplash.com/photo-1437482078695-73f5ca6c96e2?w=800"
        },
        {
            "soru": "Agaclari neden korumaliyiz?",
            "cevaplar": [
                "Dogayi korumak icin",
                "Cop atmak icin",
                "Suyu kirletmek icin"
            ],
            "dogru": 0,
            "resim": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800"
        }
    ]

    soru = random.choice(sorular)

    embed = discord.Embed(
        title="🌍 Cevre Quiz",
        description=soru["soru"],
        color=discord.Color.green()
    )
    embed.set_image(url=soru["resim"])

    for i, cevap in enumerate(soru["cevaplar"]):
        embed.add_field(
            name=f"{chr(65 + i)}",
            value=cevap,
            inline=False
        )

    view = discord.ui.View(timeout=30)

    async def secim(interaction, secilen):
        if interaction.user != ctx.author:
            await interaction.response.send_message(
                "Bu quiz senin degil!", ephemeral=True
            )
            return

        for buton in view.children:
            buton.disabled = True

        if secilen == soru["dogru"]:
            mesaj = "✅ Dogru cevap! Tebrikler!"
        else:
            mesaj = (
                "❌ Yanlis cevap! Dogru cevap: "
                + chr(65 + soru["dogru"])
                + " - "
                + soru["cevaplar"][soru["dogru"]]
            )

        await interaction.response.edit_message(view=view)
        await interaction.followup.send(mesaj)

    for i in range(3):
        buton = discord.ui.Button(
            label=chr(65 + i),
            style=discord.ButtonStyle.primary
        )

        async def tikla(interaction, secilen=i):
            await secim(interaction, secilen)

        buton.callback = tikla
        view.add_item(buton)

    await ctx.send(embed=embed, view=view)




@bot.command()
async def avant_apres(ctx):
    exemples = [
        {
            "titre": "Okyanus Kirliligi",
            "texte": "Coplerini denize atma! Denizleri korumaliyiz!",
            "image": "https://images.unsplash.com/photo-1621451537084-482c73073a0f?w=800"
        },
        {
            "titre": "Plastik Kirliligi",
            "texte": "Plastik atiklar dogaya zarar verir. Plastik kullanmayi azalt!",
            "image": "https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=800"
        },
        {
            "titre": "Cevreyi Temiz Tut!",
            "texte": "Copleri yere atma! Dogayi ve hayvanlari koru!",
            "image": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800"
        }
    ]

    secim = random.choice(exemples)

    embed = discord.Embed(
        title="🌍 " + secim["titre"],
        description=secim["texte"],
        color=discord.Color.green()
    )

    embed.set_image(url=secim["image"])

    await ctx.send(embed=embed)

    
















bot.run("YOUR_BOT_TOKEN_HERE")


