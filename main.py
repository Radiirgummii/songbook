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
    print(a)
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
            pdf.ln(fontsize*0.45)
        else:
            pdf.ln(0)
        pdf.cell(40, fontsize, txt)
        k += fontsize
        pdf.ln(fontsize*0.45)
        k += fontsize/2
    return k


def add_song(song):

    pdf.add_page()
    pdf.set_font("times", "b", fontsize * 1.2)
    pdf.cell(40, fontsize, song["Title"])
    pdf.ln(fontsize)
    l = fontsize * 2
    pdf.set_font("Courier", "", fontsize)
    for i in song["scheme"]:
        l += render_chord(song["txt"][i])
        if l < 350:
            pdf.ln(fontsize*0.6)
        else:
            pdf.add_page()
            l = 0


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
fontsize = 7
pdf = PDF('P', 'mm', 'A5')
pdf.add_font(
    family="str", fname='/usr/share/fonts/TTF/DejaVuSansMono.ttf', uni=True)
pdf.set_font("Courier", "", fontsize)


# reading Data
with open("songs.json", 'r') as f:
    data = json.load(f)
with open("index.json", 'r') as f:
    index = list(json.load(f).values())

for i in index:
    add_song(data[i])
pdf.output('songbook.pdf', 'F')
