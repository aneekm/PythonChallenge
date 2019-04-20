import os
import pickle
from urllib.request import urlopen
import zipfile

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

def l1_sol():
  # Problem: Caesar shift (+2)

  # following strings copied from the challenge site
  str_l1_1 = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc"\
             " dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq" \
             " rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu" \
             " ynnjw ml rfc spj"

  str_l1_2 = "map"

  print("Message: "  + caesar_str_decrypt(str_l1_1))
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
  # where X is uppercase, a/z is lowercase, and prints the middle character (a)

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

  # sol follows it until it finds the URL. was written incrementally and tested
  # that the index of 85 and lack of any other trick links was deterministic, 
  # so it will work everytime.

  print("start")
  base = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
  ptr = "12345"
  
  for i in range(400):
    # at the 85th link, you are directed to divide current nothing by 2 instead 
    # of searching for a new nothing
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
    print("".join([k*v for k,v in line]))

def l6_sol():
  # download zip file (look at source to get the hint)
  # sol then follows the zipped linked list, which eventually terminates
  # with a file telling us to look at the comments.
  # When the list is done, prints out comments collected.
  zipped = urlopen("http://www.pythonchallenge.com/pc/def/channel.zip").read()
  f = open("channel.zip", "wb")
  f.write(zipped)
  f.close()

  with zipfile.ZipFile("channel.zip", 'r') as myzip:
    num = '90052'
    comments = []
    
    while True:
      comments.append(myzip.getinfo(num + ".txt").comment.decode("utf-8"))
      try:
        data = myzip.read(num + '.txt').decode('utf-8')
      except KeyError:
        # This is the conclusion of the zipped list
        break;
      num = data.split()[-1]

    # print shows the word HOCKEY written with the characters: O X Y G E N
    print("".join(comments))

# HINT: going to hockey.html tells us to look at the letters
# so the next URL is oxygen.html!
  os.remove("channel.zip")


if __name__ == '__main__':
  # runs the solution I am currently working on
  l6_sol()