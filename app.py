from flask import Flask, render_template, url_for, send_file, redirect, request
from datetime import datetime
from PIL import Image
from numpy import random
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageEnhance
from io import StringIO
app = Flask(__name__)


@app.route("/memes_redir")
def showRedirMeme():
    path = request.args['messages']
    #path = "00562.jpg"
    fullpath = "./static/memes/" + path
    x = 0

    while not os.path.isfile(fullpath):
        x += 1
    print(x)
    return send_file(fullpath, mimetype="image/jpeg")

@app.route("/memes/<path:path>")
def showMeme(path):
    counter = 0
    while os.path.isdir('./static/memes/' + path) == False:
        counter += 1
        if(counter > 1000):
            return """
                <h1>Hello heroku</h1>
            """
    new_meme = Image.open("./static/under_construction.jpg")
    fullpath = "./static/memes/" + path
    new_meme.save(fullpath)
    resp = Flask.make_response(open(fullpath).read())
    resp.content_type = "image/jpeg"
    return send_file(fullpath, mimetype="image/jpeg")

@app.route("/gen_meme/cnn")
def genMeme_CNN():
    return genMeme("cnn.com")

@app.route("/gen_meme/bbc")
def genMeme_BBC():
    return genMeme("bbc.com")

@app.route("/gen_meme/wiki")
def genMeme_WIKI():
    return genMeme("wiki.com")


def genMeme(url):
    src, alt = getImageLinks(url)
    new_meme = makeMeme(src, alt)
    #new_meme = Image.open("./static/under_construction.jpg")
    img_io = StringIO()
    new_meme.save(img_io, 'JPEG', quality=90)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

    # meme_val = random.randint(0,100000)
    # meme_val = str(meme_val).zfill(5)
    #
    # path = meme_val+".jpg"
    # fullpath = "./static/memes/" + path
    #
    # new_meme.save(fullpath, "JPEG", quality=90)
    # return redirect(url_for('showRedirMeme', messages=path))

    #return send_file(fullpath,mimetype="image/jpeg")



@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    return """
    <>
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    """

def fetchImg(url):
    print("URL: " + url)
    res = requests.get(url, stream=True).raw
    img = Image.open(res)
    return img

def makeMeme(img_srcs,alt_texts):
    top_meme_text = " ".join(makeMemeText(alt_texts))
    bottom_meme_text = " ".join(makeMemeText(alt_texts))
    rand_index = random.randint(0, len(img_srcs))
    img = fetchImg((img_srcs[rand_index]))
    if random.random() > 0.9:
        img = compressImage(img)

    if random.random() > 0.3:
        img = fryImage(img)
    img_w, img_h = img.size
    y_top = 0
    y_bottom = 0
    draw = ImageDraw.Draw(img)

    # font = ImageFont.truetype(<font-file>, <font-size>)
    font_size = int(img_w/17)
    outline_col = 'black'
    text_col = 'white'
    font = ImageFont.truetype("./static/impact.ttf", font_size)
    draw_outline(img,draw, font, top_meme_text, "top", font_size, outline_col, text_col)
    draw_outline(img,draw, font, bottom_meme_text, "bottom", font_size, outline_col, text_col)
    img.save('sample-out.jpg')
    img = Image.open("sample-out.jpg")
    if random.random() > 0.9:
        img = fryImage(img)
    return img

def fryImage(picture):
    type = "JPEG"
    type_ext = ".jpg"
    brightness = random.random()
    sharpness = random.random()
    contrast = random.random()
    saturation = random.random()
    compression = random.random()

    enhancer = ImageEnhance.Brightness(picture)
    picture = enhancer.enhance(brightness * 5)
    enhancer = ImageEnhance.Sharpness(picture)
    picture = enhancer.enhance(sharpness * 100)
    enhancer = ImageEnhance.Contrast(picture)
    picture = enhancer.enhance(contrast * 20)
    enhancer = ImageEnhance.Color(picture)
    picture = enhancer.enhance(saturation * 20)
    return picture

def compressImage(picture):
    type = "JPEG"
    type_ext = ".jpg"
    enhancer = ImageEnhance.Brightness(picture)
    picture = enhancer.enhance(1.4)
    picture = picture.resize((int(picture.width / 1.45), int(picture.height / 1.45)), Image.NEAREST)
    picture.save('temp_meme'+type_ext, type, optimize=False, quality=1)
    picture = Image.open('temp_meme'+type_ext)
    picture = picture.resize((int(picture.width * 1.45), int(picture.height * 1.45)), Image.NEAREST)
    enhancer = ImageEnhance.Brightness(picture)
    picture = enhancer.enhance(0.85)
    return picture


def draw_outline(img,draw_main, font,text, pos, font_size, outline_col, text_col):
    outline_width = int(font_size/20)
#    if outline_width < 1:
    MARGIN = 10
    outline_width = 2

    tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
    img_w, img_h = img.size
    w, h = draw_main.textsize(text,font=font)
    x = (img_w - w)/2
    if pos == 'top':
        y = MARGIN
    elif pos == 'bottom':
        y = img_h-h - MARGIN

    # Create a drawing context for it.
    draw_blur = ImageDraw.Draw(tmp)
    for draw in [draw_main, draw_blur]:
        draw.text((x, y+outline_width), text, font=font, fill=outline_col)
        draw.text((x, y-outline_width), text, font=font, fill=outline_col)
        draw.text((x-outline_width, y), text, font=font, fill=outline_col)
        draw.text((x+outline_width, y), text, font=font, fill=outline_col)

        draw.text((x-outline_width, y+outline_width), text, font=font, fill=outline_col)
        draw.text((x+outline_width, y-outline_width), text, font=font, fill=outline_col)
        draw.text((x-outline_width, y-outline_width), text, font=font, fill=outline_col)
        draw.text((x+outline_width, y+outline_width), text, font=font, fill=outline_col)

    tmp = tmp.filter(ImageFilter.BLUR)

    img.paste(tmp, (0, 0), tmp)
    draw_main.text((x, y), text, font=font, fill=text_col)

def makeMemeText(text_arr):
    meme_text = []
    tagged_text_arr = []
    print(text_arr)
    for i in range(len(text_arr)):
        tagged_text_arr.append(text_arr[i].split())

    for i in range(5):
        rand_index = random.randint(0, len(text_arr))
        split_text = text_arr[rand_index].split(" ")
        print(split_text)
        if split_text[0][0].isupper():
            cont = True
            while cont is True:
                rand_index = random.randint(0, len(split_text))
                img_alt = split_text[rand_index]
                if 'photo' not in img_alt and ')' not in img_alt and '(' not in img_alt \
                        and ';' not in img_alt and '&' not in img_alt and '--' not in img_alt \
                        and 'RIVERDALE' not in img_alt and '/' not in img_alt and '--' not in img_alt:
                    meme_text.append(split_text[rand_index].upper())
                    cont = False
                else:
                    cont = True
        else:
            i -= 1
    return meme_text


def getImageLinks(URL):
    html = None
    if 'cnn' in URL:
        html = open("./static/cnn.html", "r")
    elif 'bbc' in URL:
        html = open("./static/bbc.html", "r")
    elif 'wiki' in URL:
        html = open("./static/wiki.html", "r")
    else:
        exit()

    soup = BeautifulSoup(html.read(), features="html.parser")
    html.close()

    imgs = soup.findAll("img")
    for img in imgs[:]:

        if 'cnn' in URL:
            if 'jpg' not in str(img) or 'alt=""' in str(img) or 'alt=' not in str(img) \
                    or 'data-src' not in str(img) or 'alt=" "' in str(img):
                imgs.remove(img)
        if 'bbc' in URL:
            if 'jpg' not in str(img) or 'alt=' not in str(img) or 'alt=""' in str(img) or 'production' not in str(img) :
                imgs.remove(img)
        if 'wiki' in URL:
            print(imgs)
            if 'jpg' not in str(img) or 'img-loading-hide' in str(img):
                imgs.remove(img)

    imgs_src = []
    imgs_alt = []

    for img in imgs:
        img_src = None
        if 'bbc' in URL:
            img_src = str(img)
            img_src = img_src.split('data-src="', 1)[1]
            img_src = img_src.split('"', 1)[0]
            if "{width}" in img_src:
                img_src = img_src.replace("{width}", str(800))
        if 'cnn' in URL:
            img_src = str(img)
            img_src = img_src.split('data-src="', 1)[1]
            img_src = img_src.split('"', 1)[0]
            while img_src[0] == "/":
                img_src = img_src[1:]
                img_src = img_src[1:]

                img_src= ''.join(('http://', img_src))
        imgs_src.append(img_src)
        img_alt = str(img)
        print(img_alt)
        img_alt = img_alt.split('alt="', 1)[1]
        img_alt = img_alt.split('"', 1)[0]
        imgs_alt.append(img_alt)

    return imgs_src, imgs_alt

if __name__ == '__main__':
    app.run(threaded=True)
