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

@app.route("/rank")
def rank():
    # ===== DADOS =====
    nome1 = request.args.get("nome1", "sem nome")
    nome2 = request.args.get("nome2", "sem nome")
    nome3 = request.args.get("nome3", "sem nome")
    nome4 = request.args.get("nome4", "sem nome")
    nome5 = request.args.get("nome5", "sem nome")
   

    mind1 = request.args.get("mind1", "0")
    mind2 = request.args.get("mind2", "0")
    mind3 = request.args.get("mind3", "0")
    mind4 = request.args.get("mind4", "0")
    mind5 = request.args.get("mind5", "0")

    # ===== POSIÇÕES (X/Y) =====
    nome1_x, nome1_y = arg_int("nome1_x",160), arg_int("nome1_y",60)
    nome2_x, nome2_y = arg_int("nome2_x",1000), arg_int("nome2_y",60)
    nome3_x, nome3_y = arg_int("nome3_x",1000), arg_int("nome3_y",130)
    nome4_x, nome4_y = arg_int("nome4_x",160), arg_int("nome4_y",130)
    nome5_x, nome5_y = arg_int("nome5_x",80), arg_int("nome5_y",200)
    

    mind1_x, mind1_y = arg_int("mind1_x",1020), arg_int("mind1_y",650)
    mind2_x, mind2_y = arg_int("mind2_x",860), arg_int("mind2_y",770)
    mind3_x, mind3_y = arg_int("mind3_x",1180), arg_int("mind3_y",770)
    mind4_x, mind4_y = arg_int("mind4_x",860), arg_int("mind4_y",900)
    mind5_x, mind5_y = arg_int("mind5_x",1180), arg_int("mind5_y",900)

    # ===== AVATAR =====

    
    avatar_url = request.args.get("avatar1")
    avatar1_x = arg_int("avatar_x",550)
    avatar1_y = arg_int("avatar_y",390)

    avatar_url = request.args.get("avatar2")
    avatar2_x = arg_int("avatar_x",570)
    avatar2_y = arg_int("avatar_y",410)

    avatar_url = request.args.get("avatar3")
    avatar3_x = arg_int("avatar_x",520)
    avatar3_y = arg_int("avatar_y",360)

    avatar_url = request.args.get("avatar4")
    avatar4_x = arg_int("avatar_x",600)
    avatar4_y = arg_int("avatar_y",440)

    avatar_url = request.args.get("avatar5")
    avatar5_x = arg_int("avatar_x",650)
    avatar5_y = arg_int("avatar_y",490)

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
    draw.text((nome1_x,nome1_y), nome1, fill="black", font=font)
    draw.text((nome2_x,nome2_y), nome2, fill="black", font=font)
    draw.text((nome3_x,nome3_y), nome3, fill="black", font=font)
    draw.text((nome4_x,nome4_y), nome4, fill="black", font=font)
    draw.text((nome5_x,nome5_y), nome5, fill="black", font=font)
    

    draw.text((mind1_x,mind1_y), mind1, fill="black", font=font_small)
    draw.text((mind2_x,mind2_y), mind2, fill="black", font=font_small)
    draw.text((mind3_x,mind3_y), mind3, fill="black", font=font_small)
    draw.text((mind4_x,mind4_y), mind4, fill="black", font=font_small)
    draw.text((mind5_x,mind5_y), mind5, fill="black", font=font_small)

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
