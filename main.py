import json
from fpdf import FPDF

# Functions


class PDF(FPDF):
    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', '', fontsize)
        # Print current and total page numbers
        if pdf.page_no() > 1:
            self.cell(0, 10, str(pdf.page_no()-1), 0, 0, "C")


def render_verse(txt, rchords=False):
    a = txt.split("%")
    b = []
    utxt = ""
    for z, i in zip(a, range(len(a))):
        b.append([])
        x = []
        a = z.split("}")
        for j in a:
            x.append(j.split("{"))
        b[i].extend(x)
        for i in b:
            chords = ""
            txt = ""
            l = 0
            for j in i:
                if len(j) == 1:
                    txt += j[0]
                else:
                    if l > 0:
                        chords += " " * (len(j[0])-l) + j[1]
                        if j[0] != " ":
                            txt += j[0]
                        l = len(j[1])
                    else:
                        chords += " " * (len(j[0])) + j[1]
                        txt += j[0]
                        l = len(j[1])
        if rchords:
            if chords != "":
                pdf.cell(0, fontsize, chords)
                pdf.ln(fontsize*0.3)
            else:
                pdf.ln(0)
            pdf.cell(0, fontsize, txt)
            pdf.ln(fontsize*0.33)
        else:
            utxt += txt + " "
    if not rchords:

        txt = pdf.multi_cell(0, fontsize*0.35, utxt, 0, "J", 0, True)
        for i in txt:
            pdf.cell(0, 0, i)
            pdf.ln(fontsize*0.35)
    pdf.ln(sbv)


def add_song(data, title):
    global pagenumbers, img, noimg, rimg, form

    # add page if song has 2 pages so you would have to scroll
    h = 18
    for i in data[title]["scheme"]:
        h += (data[title]["txt"][i].count("%")+1)*5.75+4
    if h > 188 and pdf.page_no() % 2 == 0 and form != "A6":
        pdf.add_page()
        if rimg:
            try:
                pdf.image(f"./pictures/{img}.jpg", 10, 10, 128, 180)
                img += 1
            except:
                noimg = True
    # add Title
    pdf.add_page()
    pdf.set_font("times", "b", fontsize * 1.2)
    pdf.cell(0, fontsize, title)
    pdf.ln(fontsize*1.5)
    l = fontsize * 2
    pdf.set_font("Courier", "", fontsize)
    a = {title: pdf.page_no()-1}
    pagenumbers.update(a)
    h = fontsize * 0.9
    l = 0
    for i in data[title]["scheme"]:
        if pdf.get_y() + (data[title]["txt"][i].count("%") * fontsize * 0.65) + 10 >= 188 and rchords:
            l = pdf.get_y()-10.00125
            pdf.add_page()
            h = data[title]["txt"][i].count(
                "%") * fontsize * 0.6 + fontsize * 0.55
        elif pdf.get_y() + (len(pdf.multi_cell(0, 10, data[title]['txt'][i], 0, 'J', 0, True)) * fontsize * 0.35) > 130 and not rchords:
            pdf.add_page()

        render_verse(data[title]["txt"][i], rchords)
    print(f'sucsessfully added song "{title}" on page {pdf.page_no()-1}')


def create_index(index):
    pdf.add_page()
    pdf.set_font("times", "b", fontsize * 1.2)
    pdf.cell(40, fontsize, "Index")
    pdf.ln(fontsize*0.9)
    pdf.set_font("Courier", "", fontsize)
    for i in index.items():
        pdf.cell(40, fontsize, f"{i[0]+' ' * (40-len(i[0]))}{i[1]}")
        pdf.ln(fontsize * 0.4)
    print("sucsessfully added index")


# init vars
fontsize = 9
form = input("wich format do you want to use? ")
print(form)
if form == "A6":
    pdf = PDF('P', 'mm', (105, 148))
    pagesize = 148  # pageheight
    rchords = False  # render Chords
    sbv = fontsize*0.3  # space between verses
else:
    pdf = PDF('P', 'mm', "A5")
    pagesize = 210  # pageheight
    rchords = True  # render Chords
    sbv = fontsize * 0.3  # space between verses
pagenumbers = {}
img = 1
noimg = False

# reading Data
with open("songs.json", 'r') as f:
    data = json.load(f)

# Config
print("please choose your index:")
for i, name in zip(range(len(data["index"])), data["index"].keys()):
    print(f"{i+1} : {name}")
index = data["index"][list(data["index"].keys())[int(input())-1]]

a = input("do you want to add images?")
if a == "y" or a == "Y" or a == "yes" or a == "Yes" or a == "true" or a == "True":
    rimg = True
else:
    rimg = False


# Add title page
pdf.add_page()
pdf.set_xy(10, pagesize*0.5)
pdf.set_font("times", "", 60)
pdf.cell(0, 10, "Liederbuch", 0, 0, "C")

# Add songs
for i in index:
    add_song(data, i)

create_index(pagenumbers)


# Output pdf
pdf.output('songbook.pdf', 'F')
if noimg:
    print(
        f"you dont have enouth correctly named images in the pictures folder you need {img}.")
print('sucsessfully outputted songbook as "songbook.pdf"')
