import json as json
from fpdf import FPDF
import os
# Functions


class PDF(FPDF):
    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', 'I', fontsize)
        # Print current and total page numbers
        self.cell(130, 10, str(pdf.page_no()), 0, 0, "C")


def render_chord(txt):
    a = txt.split("%")
    b = []
    ftxt = ""
    k = 0

    # split lines seperated by %
    for z, i in zip(a, range(len(a))):
        b.append([])
        x = []
        a = z.split("}")
        for j in a:
            x.append(j.split("{"))
        b[i].extend(x)
        a = []
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
                        txt += j[0]
                        l = len(j[1])
                    else:
                        chords += " " * (len(j[0])) + j[1]
                        txt += j[0]
                        l = len(j[1])
        pdf.cell(40, fontsize, chords)
        if chords != "":
            pdf.ln(fontsize*0.3)
        else:
            pdf.ln(0)
        pdf.cell(40, fontsize, txt)
        pdf.ln(fontsize*0.35)


def add_song(data, title):
    global pagenumbers, pictures, picnb

    # add page if song has 2 pages so you would have to scroll
    h = fontsize * 0.9
    for i in data[title]["scheme"]:
        h += data[title]["txt"][i].count("%") * fontsize * 0.6
        h += fontsize * 0.55
    if h >= 150 and pdf.page_no() % 2 == 0:
        pdf.add_page()
        pdf.image(f"../pictures/{pictures[picnb]}", 10, 10, 128, 180)
        picnb += 1

    # add Title
    pdf.add_page()
    pdf.set_font("times", "b", fontsize * 1.2)
    pdf.cell(40, fontsize, title)
    pdf.ln(fontsize*0.9)
    l = fontsize * 2
    pdf.set_font("Courier", "", fontsize)
    a = {title: pdf.page_no()}
    pagenumbers.update(a)
    h = fontsize * 0.9
    for i in data[title]["scheme"]:
        if pdf.get_y() + (data[title]["txt"][i].count("%") * fontsize * 0.65) + 10 >= 190:
            pdf.add_page()
            h = data[title]["txt"][i].count(
                "%") * fontsize * 0.6 + fontsize * 0.55
        render_chord(data[title]["txt"][i])
        pdf.ln(fontsize*0.55)
    print(f'sucsessfully added song "{title}"')


def create_index(index):
    pdf.add_page()
    pdf.add_page()
    pdf.set_font("times", "b", fontsize * 1.2)
    pdf.cell(40, fontsize, "Index")
    pdf.ln(fontsize*0.9)
    l = fontsize * 2
    pdf.set_font("Courier", "", fontsize)
    for i in index.items():

        pdf.cell(40, fontsize, f"{i[0]+' ' * (40-len(i[0]))}{i[1]}")
        pdf.ln(fontsize * 0.3)
    print("sucsessfully added index")


# init vars
fontsize = 9
pdf = PDF('P', 'mm', 'A5')
pagenumbers = {}
pictures = os.listdir("../pictures")
picnb = 0

# reading Data
with open("songs.json", 'r') as f:
    data = json.load(f)
print("please choose your index:")
for i , name in zip(range(len(data["index"])),data["index"].keys()):
    print(f"{i+1} : {name}")
print(list(data["index"].keys()))
index = data["index"][list(data["index"].keys())[int(input())-1]]

# Add title page
pdf.add_page()
pdf.set_xy(0, 100)
pdf.set_font("times", "", 80)
pdf.cell(148, 10, "Liederbuch", 0, 0, "C")

# Add songs
for i in index:
    add_song(data, i)

create_index(pagenumbers)

# Output pdf
pdf.output('songbook.pdf', 'F')
print('sucsessfully outputted songbook as "songbook.pdf"')
