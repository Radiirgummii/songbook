import json as json
from fpdf import FPDF
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
        k += fontsize
        if chords != "":
            pdf.ln(fontsize*0.3)
        else:
            pdf.ln(0)
        pdf.cell(40, fontsize, txt)
        k += fontsize
        pdf.ln(fontsize*0.35)
        k += fontsize/2
    return k


def add_song(data,title):
    #add page if song has 2 pages so you would have to scroll
    h = fontsize * 0.9
    for i in data[title]["scheme"]:
        h += data[title]["txt"][i].count("%") * fontsize * 0.6
        h += fontsize * 0.55
    if h >= 150 and pdf.page_no() % 2 == 1:
        pdf.add_page() 
    

    #add Title
    pdf.add_page()
    pdf.set_font("times", "b", fontsize * 1.2)
    pdf.cell(40, fontsize, title)
    pdf.ln(fontsize*0.9)
    l = fontsize * 2
    pdf.set_font("Courier", "", fontsize)

    h = fontsize * 0.9
    for i in data[title]["scheme"]:
        h += data[title]["txt"][i].count("%") * fontsize * 0.6 + fontsize * 0.55
        if h >= 140:
            pdf.add_page()
            h = data[title]["txt"][i].count("%") * fontsize * 0.6 + fontsize * 0.55
        render_chord(data[title]["txt"][i])
        pdf.ln(fontsize*0.55)


def create_index(index, data):
    j = 0
    pdf.add_page()
    for i in index:
        if j > 30:
            pdf.add_page()
        a = 1  # data[i]['Title']
        pdf.cell(40, fontsize, f"{data[i]['Title']}")
        pdf.ln(fontsize/2)
        j += 1


# init vars
fontsize = 9
pdf = PDF('P', 'mm', 'A5')
pdf.add_font(
    family="str", fname='/usr/share/fonts/TTF/DejaVuSansMono.ttf', uni=True)
pdf.set_font("Courier", "", fontsize)


# reading Data
with open("songs.json", 'r') as f:
    data = json.load(f)
index = data["index"]

for i in index:
    add_song(data,i)
pdf.output('songbook.pdf', 'F')
