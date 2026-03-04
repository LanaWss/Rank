from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = Flask(__name__)

def arg_int(name, default):
    try:
        return int(request.args.get(name, default))
    except:
        return default

@app.route("/ficha")
def ficha():
    # ===== DADOS =====
    nome = request.args.get("nome", "Desconhecido")
    idade = request.args.get("idade", "?")
    genero = request.args.get("genero", "?")
    ocupacao = request.args.get("ocupacao", "?")
    raca = request.args.get("raca", "?")
    naipe = request.args.get("naipe", "?")
    ataque = request.args.get("ataque", "0")
    defesa = request.args.get("defesa", "0")
    historia = request.args.get("historia", "Nenhuma")

    forca = request.args.get("forca", "0")
    carisma = request.args.get("carisma", "0")
    intelecto = request.args.get("intelecto", "0")
    agilidade = request.args.get("agilidade", "0")
    percepcao = request.args.get("percepcao", "0")

    # ===== POSIÇÕES (X/Y) =====
    nome_x, nome_y = arg_int("nome_x",160), arg_int("nome_y",60)
    idade_x, idade_y = arg_int("idade_x",1000), arg_int("idade_y",60)
    genero_x, genero_y = arg_int("genero_x",1000), arg_int("genero_y",130)
    ocupacao_x, ocupacao_y = arg_int("ocupacao_x",160), arg_int("ocupacao_y",130)
    raca_x, raca_y = arg_int("raca_x",80), arg_int("raca_y",200)
    naipe_x, naipe_y = arg_int("naipe_x",1000), arg_int("naipe_y",200)
    ataque_x, ataque_y = arg_int("ataque_x",80), arg_int("ataque_y",270)
    defesa_x, defesa_y = arg_int("defesa_x",500), arg_int("defesa_y",270)
    historia_x, historia_y = arg_int("historia_x",130), arg_int("historia_y",350)

    forca_x, forca_y = arg_int("forca_x",1020), arg_int("forca_y",650)
    carisma_x, carisma_y = arg_int("carisma_x",860), arg_int("carisma_y",770)
    intelecto_x, intelecto_y = arg_int("intelecto_x",1180), arg_int("intelecto_y",770)
    agilidade_x, agilidade_y = arg_int("agilidade_x",860), arg_int("agilidade_y",900)
    percepcao_x, percepcao_y = arg_int("percepcao_x",1180), arg_int("percepcao_y",900)

    # ===== AVATAR =====
    avatar_url = request.args.get("avatar")
    avatar_x = arg_int("avatar_x",520)
    avatar_y = arg_int("avatar_y",360)
    avatar_size = arg_int("avatar_size",300)
    avatar_round = request.args.get("avatar_round", "true").lower() == "true"

    # ===== FONTES =====
    font_size = arg_int("font_size",36)
    font_small_size = arg_int("font_small",28)

    base = Image.open("base.png").convert("RGBA")
    draw = ImageDraw.Draw(base)

    try:
        font = ImageFont.truetype("font.ttf", font_size)
        font_small = ImageFont.truetype("font.ttf", font_small_size)
    except:
        font = ImageFont.load_default()
        font_small = font

    # ===== TEXTOS =====
    draw.text((nome_x,nome_y), nome, fill="black", font=font)
    draw.text((idade_x,idade_y), idade, fill="black", font=font)
    draw.text((genero_x,genero_y), genero, fill="black", font=font)
    draw.text((ocupacao_x,ocupacao_y), ocupacao, fill="black", font=font)
    draw.text((raca_x,raca_y), raca, fill="black", font=font)
    draw.text((naipe_x,naipe_y), naipe, fill="black", font=font)
    draw.text((ataque_x,ataque_y), ataque, fill="black", font=font)
    draw.text((defesa_x,defesa_y), defesa, fill="black", font=font)
    draw.text((historia_x,historia_y), historia, fill="black", font=font_small)

    draw.text((forca_x,forca_y), forca, fill="black", font=font_small)
    draw.text((carisma_x,carisma_y), carisma, fill="black", font=font_small)
    draw.text((intelecto_x,intelecto_y), intelecto, fill="black", font=font_small)
    draw.text((agilidade_x,agilidade_y), agilidade, fill="black", font=font_small)
    draw.text((percepcao_x,percepcao_y), percepcao, fill="black", font=font_small)

    # ===== AVATAR =====
    if avatar_url:
        try:
            r = requests.get(avatar_url, timeout=5)
            avatar = Image.open(BytesIO(r.content)).convert("RGBA")
            avatar = avatar.resize((avatar_size, avatar_size))

            if avatar_round:
             base.paste(avatar, (avatar_x, avatar_y), avatar)
        except:
            pass

    output = BytesIO()
    base.save(output, format="PNG")
    output.seek(0)

    return send_file(output, mimetype="image/png")

if __name__ == "__main__":
    app.run()
