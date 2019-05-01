import os
import pickle
from urllib.request import urlopen
import zipfile
import requests
import shutil
from PIL import Image, ImageDraw
import bz2
from xmlrpc import client
import datetime
from io import BytesIO
import numpy as np


def hanoi(n, src, dest, spare):
    if n == 1:
        dest.append(src.pop())
        return

    hanoi(n-1, src, spare, dest)

    dest.append(src.pop())

    hanoi(n-1, spare, dest, src)


def caesar_char(c, shift):
    asciiNum = ord(c) + shift
    asciiNum = asciiNum if asciiNum > 96 else asciiNum + 26
    asciiNum = asciiNum if asciiNum < 123 else asciiNum - 26
    return chr(asciiNum)


def caesar_str_decrypt(str, shift):
    ret = ""
    for i in str:
        ret += caesar_char(i, 2) if i.isalpha() else i
    return ret


def conway(x, start):
    cur = start

    # do x iterations to get xth conway number
    for i in range(x):
        nxt = []
        char = cur[0]
        count = 0
        for c in cur:
            if char == c:
                count += 1
            else:
                nxt.append(str(count))
                nxt.append(char)
                char = c
                count = 1
        nxt.append(str(count))
        nxt.append(char)

        cur = ''.join(nxt)

    return cur


def l1_sol():
    # Problem: Caesar shift (+2)

    # following strings copied from the challenge site
    str_l1_1 = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr"         \
                " amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr"    \
                " ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle"               \
                " qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj"

    str_l1_2 = "map"

    print("Message: " + caesar_str_decrypt(str_l1_1))
    print("Next URL: " + caesar_str_decrypt(str_l1_2))


def l2_sol():
    # Problem: look for letters in html file
    # This solution looks for all leters, so the HTML is also printed out.
    # Ignore everything except the very last line of output for the next URL

    data = urlopen("http://www.pythonchallenge.com/pc/def/ocr.html").read() \
        .decode()
    f = data.splitlines()

    for x in f:
        filtered = ""
        for i in x:
            if i.isalpha():
                filtered += i
                if (len(filtered) > 0):
                    if (len(filtered) > 1):
                        print(filtered)
                    else:
                        print(filtered, end="")
    print("\n|-----end-----|")


def l3_sol():
    # looks for pattern in html file that fit: <zXXXaXXXz>
    # where X is uppercase, a/z is lowercase, and prints the middle character

    data = urlopen("http://www.pythonchallenge.com/pc/def/equality.html") \
        .read().decode()
    f = data.splitlines()

    for x in f:
        filtered = ""
        for i in range(len(x)-8):
            if (x[i].islower() and x[i+1:i+4].isupper() and x[i+4].islower()
                    and x[i+5:i+8].isupper() and x[i+8].islower()):
                filtered += x[i+4]
            if (len(filtered) > 0):
                print(filtered, end="")
    print("\n|-----end-----|")


def l4_sol():
    # linkedlist of URLs

    # sol follows it until it finds the URL. was written incrementally
    # and tested that the index of 85 and lack of any other trick links
    # was deterministic, so it will work everytime.

    print("start")
    base = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
    ptr = "12345"

    for i in range(400):
        # at the 85th link, you are directed to divide current nothing
        # by 2 instead of searching for a new nothing
        if i == 85:
            ptr = str(int(ptr) / 2)
            continue

        url = base + ptr
        response = urlopen(url)
        html = response.read()
        vals = html.split()
        ptr = vals[-1].decode('utf-8')
        print(str(i) + "::" + html.decode('utf-8') + "->" + ptr)

        # after index 85, the next link with no numeric nothing is the solution
        try:
            int(ptr)
        except ValueError:
            print("next URL: " + ptr)


def l5_sol():
    # "peak hell" -> pickle, a Python lib for serializng data

    # link found in HTML source of challenge site
    pickled = urlopen("http://www.pythonchallenge.com/pc/def/banner.p")
    list_of_tuples = pickle.load(pickled)

    for line in list_of_tuples:
        print("".join([k*v for k, v in line]))


def l6_sol():
    # download zip file (look at source to get the hint)
    # sol then follows the zipped linked list, which eventually terminates
    # with a file telling us to look at the comments.
    # When the list is done, prints out comments collected.
    zipped = urlopen("http://www.pythonchallenge.com/pc/def/channel.zip") \
        .read()
    f = open("channel.zip", "wb")
    f.write(zipped)
    f.close()

    with zipfile.ZipFile("channel.zip", 'r') as myzip:
        num = '90052'
        comments = []

        while True:
            comments.append(myzip.getinfo(num + ".txt")
                            .comment.decode("utf-8"))
            try:
                data = myzip.read(num + '.txt').decode('utf-8')
            except KeyError:
                # This is the conclusion of the zipped list
                break
            num = data.split()[-1]

        # print shows the word HOCKEY written with the characters: O X Y G E N
        print("".join(comments))

# HINT: going to hockey.html tells us to look at the letters
# so the next URL is oxygen.html!
    os.remove("channel.zip")


def l7sol():
    r = requests.get('http://www.pythonchallenge.com/pc/def/oxygen.png',
                     stream=True)
    with open('img.png', 'wb') as img:
        shutil.copyfileobj(r.raw, img)

    img = Image.open('img.png', 'r')

    # grayscale code is in the middle row of pixels
    row = []
    for w in range(img.width):
        color = img.getpixel((w, img.height/2))
        if color[0] == color[1] and color[1] == color[2]:
            row.append(color[0])

    chrs = [chr(c) for c in row[::7]]
    print(*chrs, sep='')

    # list taken from output of previous print
    nxtlvl = [105, 110, 116, 101, 103, 114, 105, 116, 121]
    nxtchrs = [chr(x) for x in nxtlvl]
    print("URL: ", end='')
    print(*nxtchrs, sep='')

    img.close()
    os.remove('img.png')


def l8sol():
    # taken from page source:
    un = b'BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084'
    pw = b'BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08'

    print(bz2.decompress(un))
    print(bz2.decompress(pw))


def l9sol():
    r = requests.get('http://www.pythonchallenge.com/pc/return/good.html',
                     auth=('huge', 'file'))

    fIdx = r.text.find('first:')
    sIdx = r.text.find('second:', fIdx)
    endIdx = r.text.find('-->', sIdx)

    fStr = r.text[fIdx + 7:sIdx - 2].replace("\n", "")
    sStr = r.text[sIdx + 8:endIdx - 2].replace("\n", "")

    first = [int(i) for i in fStr.split(',')]
    second = [int(i) for i in sStr.split(',')]

    im = Image.new('RGB', (500, 500))
    draw = ImageDraw.Draw(im)
    draw.polygon(first, fill='white')
    draw.polygon(second, fill='white')
    im.show()


def l10sol():
    # clicking link takes us to another URL which has the starting numbers of
    # Conway's sequence. Prompt is len(a[30]) = ?. We must generate the
    # 30th conway's number and get its length.

    print(len(conway(30, "1")))


def l11sol():
    r = requests.get('http://www.pythonchallenge.com/pc/return/cave.jpg',
                     auth=('huge', 'file'),
                     stream=True)

    with open('img.png', 'wb') as img:
        shutil.copyfileobj(r.raw, img)

    img = Image.open('img.png', 'r')
    odd = Image.new('RGB', (img.width // 2, img.height // 2))
    counter = 0
    for row in range(img.height):
        for col in range(img.width):
            loc = (col, row)
            loc_new = (col // 2, row // 2)
            pix = img.getpixel(loc)
            # make the pixel brighter since it's so dark
            pix = (pix[0] + 100, pix[1] + 100, pix[2] + 100)
            if counter % 2 == 1:
                odd.putpixel(loc_new, pix)
            counter += 1
    odd.show()

    img.close()
    os.remove('img.png')


def l12sol():
    r = requests.get('http://www.pythonchallenge.com/pc/return/evil2.gfx',
                     auth=('huge', 'file'),
                     stream=True)
    with open('evil2.gfx', 'wb') as gfx:
        shutil.copyfileobj(r.raw, gfx)

    with open('evil2.gfx', 'rb') as gfx:
        data = gfx.read()

        for i in range(5):
            open('%d.jpg' % i, 'wb').write(data[i::5])

    input("Press Enter after viewing images 0-4.jpg to get next URL")

    os.remove('evil2.gfx')
    for i in range(5):
        os.remove('%d.jpg' % i)


def l13sol():
    url = "http://www.pythonchallenge.com/pc/phonebook.php"
    with client.ServerProxy(url) as proxy:
        print(proxy.phone('Bert'))


def l14sol():
    r = requests.get('http://www.pythonchallenge.com/pc/return/wire.png',
                     auth=('huge', 'file'),
                     stream=True)
    with open('img.png', 'wb') as img:
        shutil.copyfileobj(r.raw, img)

    img = Image.open('img.png')
    new = Image.new('RGB', (100, 100))

    og_loc = 0
    loc = (-1, 0)
    step_val = 100
    step_num = 1
    step_direction = 0
    step_shift = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while step_val != 0:
        for i in range(step_val):
            loc = (loc[0] + step_shift[step_direction][0],
                   loc[1] + step_shift[step_direction][1])
            new.putpixel(loc, img.getpixel((og_loc, 0)))
            og_loc += 1
        step_direction = (step_direction + 1) % 4
        step_num += 1
        if step_num == 2:
            step_num = 0
            step_val -= 1

    new.show()
    os.remove('img.png')

    # above image shows a cat. going to that url tells us his name is
    # uzi <-- which is the next url.


def l15sol():
    # image shows a calendar with January 1xx6. So the year is 1__6.
    # February 29th is the same year, so a leap year.
    # Also, Jan 1st is a Thursday.
    # All the years that fit this list are:
    years = [year for year in range(1016, 1996, 20) if
             datetime.date(year, 1, 1).isoweekday() == 4]

    # Source also includes hint:
    # "he ain't the youngest, he is the second" ie. second youngest year
    year = years[-2]

    # Source includes hint:
    # "todo: buy flowers for tomorrow"
    print(datetime.date(year, 1, 27))

    # Above date is Mozart's birthday!


def l16sol():
    r = requests.get('http://www.pythonchallenge.com/pc/return/mozart.gif',
                     auth=('huge', 'file'))

    img = Image.open(BytesIO(r.content))

    pixels = [pix for pix in list(enumerate(img.histogram())) if pix[1] != 0]
    idx = [x for x in pixels if x[1] % img.height == 0]
    color = idx[0][0]

    np.array()

    for row in np.array(img):
        pink_idx = row.tolist().index(color)
        


if __name__ == '__main__':
    # runs the solution I am currently working on
    l16sol()
