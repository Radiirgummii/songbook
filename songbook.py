from fpdf import FPDF #type: ignore



class SONGBOOK(FPDF):
    def __init__(self, form:str='A5', index:str="all with testing", fontsize:int=9, renderimg:bool=False, data:dict={}):
        self.index: list = data["index"][index]
        self.fontsize:int = fontsize
        self.rimg:bool = renderimg
        self.form:str = form
        self.data:dict = data
        if form == "A6":
            super().__init__(self, 'P', 'mm', (105, 148))
            self.pagesize:int = 148  # pageheight
            self.renderchords: bool = False  # render Chords
            self.sbv = fontsize*0.3  # space between verses
        else:
            super().__init__(orientation='P', unit='mm', format='A5')
            self.pagesize = 210  # pageheight
            self.renderchords = True  # render Chords
            self.sbv = fontsize * 0.3  # space between verses
        self.pagenumbers:dict = {}
        self.img:int = 1
        self.noimg:bool = False

        # Add title page
        self.add_page()
        self.set_xy(10, self.pagesize*0.5)
        self.set_font("times", "", 60)
        self.cell(0, 10, "Liederbuch", 0, 0, "C")


    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', self.fontsize)
        if self.page_no() > 1:
            self.cell(0, 10, str(self.page_no()-1), 0, 0, "C")

    def render_verse(self,txt:str, renderchords:bool=False) -> None:
        lines: list = txt.split("%")
        splituplines:list[list[str]]= []
        formatted:str=""
        for line in lines:
            line = line.split("{")
            splitupline: list[str] = []
            for i in line:
                splitupline.append(i.split("}"))
            splituplines.append(splitupline)
        for line in splituplines:
            chordline: str = ""
            textline: str = ""
            for segment in line:
                if len(segment) <= 1:
                    textline += segment[0]
                    chordline += " "* len(segment[0])
                else:
                    chordline += segment[0] + " " * (len(segment[1])-len(segment[0]))
                    textline += segment[1]
            if renderchords:
                formatted += f"{chordline}\n{textline}\n"
            else:
                formatted += f"{textline} "
        self.multi_cell(0,self.fontsize*0.33, formatted)
        self.ln(self.sbv)
        print(self.fontsize)

    def add_song(self,title):
        global pagenumbers, img, noimg, rimg, form

        # add page if song has 2 pages so you would have to scroll
        h = 18
        for i in self.data[title]["scheme"]:
            h += (self.data[title]["txt"][i].count("%")+1)*5.75+4
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
        for i in self.data[title]["scheme"]:
            if self.get_y() + (self.data[title]["txt"][i].count("%") * self.fontsize * 0.65) >= 190 and self.renderchords:
                self.add_page()
                h = self.data[title]["txt"][i].count(
                    "%") * self.fontsize * 0.6 + self.fontsize * 0.55
            elif self.get_y() + (len(self.multi_cell(0, 10, self.data[title]['txt'][i], 0, 'J', 0, True)) * self.fontsize * 0.35) > 130 and not self.renderchords:
                self.add_page()

            self.render_verse(self.data[title]["txt"][i], self.renderchords)
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


    def build_songbook(self):
        for i in self.index:
            self.add_song(i)

    def output(self, name='songbook.pdf', dest='F'):
        self.create_index()
        super().output(name, dest)
        if self.noimg:
            print(
                f"you dont have enouth correctly named images in the pictures folder you need {img}.")
            print('successfully outputted songbook as "songbook.pdf"')
