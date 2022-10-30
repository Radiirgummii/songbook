from fpdf import FPDF


class SONGBOOK(FPDF):
    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', '', self.fontsize)
        # Print current and total page numbers
        if self.page_no() > 1:
            self.cell(0, 10, str(self.page_no()-1), 0, 0, "C")

    def render_verse(self, txt, rchords=False):
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
                    self.cell(0, self.fontsize, chords)
                    self.ln(self.fontsize*0.3)
                else:
                    self.ln(0)
                self.cell(0, self.fontsize, txt)
                self.ln(self.fontsize*0.33)
            else:
                utxt += txt + " "
        if not rchords:

            txt = self.multi_cell(0, fontsize*0.35, utxt, 0, "J", 0, True)
            for i in txt:
                self.cell(0, 0, i)
                self.ln(fontsize*0.35)
        self.ln(self.sbv)

    def add_song(self, data, title):
        global pagenumbers, img, noimg, rimg, form

        # add page if song has 2 pages so you would have to scroll
        h = 18
        for i in data[title]["scheme"]:
            h += (data[title]["txt"][i].count("%")+1)*5.75+4
        if h > 188 and self.page_no() % 2 == 0 and self.form != "A6":
            self.add_page()
            if self.rimg:
                try:
                    self.image(f"./pictures/{img}.jpg", 10, 10, 128, 180)
                    self.img += 1
                except:
                    self.noimg = True
        # add Title
        self.add_page()
        self.set_font("times", "b", self.fontsize * 1.2)
        self.cell(0, self.fontsize, title)
        self.ln(self.fontsize*1.5)
        l = self.fontsize * 2
        self.set_font("Courier", "", self.fontsize)
        a = {title: self.page_no()-1}
        self.pagenumbers.update(a)
        h = self.fontsize * 0.9
        l = 0
        for i in data[title]["scheme"]:
            if self.get_y() + (data[title]["txt"][i].count("%") * self.fontsize * 0.65) + 10 >= 188 and self.rchords:
                l = self.get_y()-10.00125
                self.add_page()
                h = data[title]["txt"][i].count(
                    "%") * self.fontsize * 0.6 + self.fontsize * 0.55
            elif self.get_y() + (len(self.multi_cell(0, 10, data[title]['txt'][i], 0, 'J', 0, True)) * self.fontsize * 0.35) > 130 and not self.rchords:
                self.add_page()

            self.render_verse(data[title]["txt"][i], self.rchords)
        print(f'sucsessfully added song "{title}" on page {self.page_no()-1}')

    def create_index(self):
        self.add_page()
        self.set_font("times", "b", self.fontsize * 1.2)
        self.cell(40, self.fontsize, "Index")
        self.ln(self.fontsize*0.9)
        self.set_font("Courier", "", self.fontsize)
        for i in self.pagenumbers.items():
            self.cell(40, self.fontsize, f"{i[0]+' ' * (40-len(i[0]))}{i[1]}")
            self.ln(self.fontsize * 0.4)
        print("sucsessfully added index")

    def __init__(self, form='A4', index="all with testing", fontsize=9, rimg=False, data={}):
        self.index = data["index"][index]
        self.fontsize = fontsize
        self.rimg = rimg
        self.form = form
        self.data = data
        if form == "A6":
            super().__init__(self, 'P', 'mm', (105, 148))
            self.pagesize = 148  # pageheight
            self.rchords = False  # render Chords
            self.sbv = fontsize*0.3  # space between verses
        else:
            super().__init__(orientation='P', unit='mm', format='A4')
            self.pagesize = 210  # pageheight
            self.rchords = True  # render Chords
            self.sbv = fontsize * 0.3  # space between verses
        self.pagenumbers = {}
        self.img = 1
        self.noimg = False

        # Add title page
        self.add_page()
        self.set_xy(10, self.pagesize*0.5)
        self.set_font("times", "", 60)
        self.cell(0, 10, "Liederbuch", 0, 0, "C")

    def build_songbook(self):
        for i in self.index:
            self.add_song(self.data, i)

    def output(self, name='songbook.pdf', dest='F'):
        self.create_index()
        super().output(name, dest)
        if self.noimg:
            print(
                f"you dont have enouth correctly named images in the pictures folder you need {img}.")
            print('successfully outputted songbook as "songbook.pdf"')
