from fpdf import FPDF  # type: ignore
import json
from colorama import Fore, Style  # type: ignore
from os import rename
from time import time


def render_verse(txt: str, renderchords: bool = True) -> str:
    lines: list = txt.split("%")
    splituplines: list[list[str]] = []
    formatted: str = ""
    for line in lines:
        line = line.split("{")
        splitupline: list[str] = []
        for segment in line:
            # if len splitupline[x] = 1 only text if len = 2 first chord then text segment
            splitupline.append(segment.split("}"))
        splituplines.append(splitupline)
    for line in splituplines:
        chordline: str = ""
        textline: str = ""
        for segment in line:
            if len(segment) <= 1:
                textline += segment[0]
                chordline += " " * len(segment[0])
            else:
                chordline += segment[0] + " " * \
                    (len(segment[1])-len(segment[0]))
                textline += segment[1]
        if renderchords:
            formatted += f"{chordline}\n{textline}\n"
        else:
            formatted += f"{textline} "
    return formatted


class SONGBOOK(FPDF):
    def __init__(self, form: str = 'A5', index: str = "all with testing", fontsize: int = 9, renderimg: bool = False, data: dict = {}):
        self.index: list = data["index"][index]
        self.fontsize: int = fontsize
        self.rimg: bool = renderimg
        self.form: str = form
        self.data: dict = data
        if form == "A6":
            super().__init__(self, 'P', 'mm', (105, 148))
            self.pagesize: int = 148  # pageheight
            self.renderchords: bool = False  # render Chords
            self.sbv = fontsize*0.3  # space between verses
        else:
            super().__init__(orientation='P', unit='mm', format='A5')
            self.pagesize = 210  # pageheight
            self.renderchords = True  # render Chords
            self.sbv = fontsize * 0.3  # space between verses
        self.pagenumbers: dict = {}
        self.img: int = 1
        self.noimg: bool = False

        # Add title page
        self.add_page()
        self.set_xy(10, self.pagesize*0.5)
        self.set_font("times", "", 60)
        self.cell(0, 10, "Liederbuch", 0, 0, "C")

    def accept_page_break(self):
        pass

    def customfooter(self):
        self.set_y(-15)
        self.set_font('Arial', '', self.fontsize)
        if self.page_no() > 1:
            self.cell(0, 10, str(self.page_no()-1), 0, 0, "C")
        self.set_font("Courier", "", self.fontsize)

    def add_song(self, title):
        global pagenumbers, img, noimg, rimg, form

        # add page if song has 2 pages so you would have to scroll
        h = 18
        for i in self.data["songs"][title]["scheme"]:
            h += (self.data["songs"][title]["txt"][i].count("%")+1)*5.75+4
        if h > 188 and self.page_no() % 2 == 0 and self.form != "A6":
            self.customfooter()
            self.add_page()
            if self.rimg:
                try:
                    self.image(f"./pictures/{img}.jpg", 10, 10, 128, 180)
                    self.img += 1
                except:
                    self.noimg = True
        # add Titel
        self.customfooter()
        self.add_page()
        self.set_font("times", "b", self.fontsize * 1.2)
        self.cell(0, self.fontsize, title)
        self.ln(self.fontsize*1.5)
        l = self.fontsize * 2
        self.set_font("Courier", "", self.fontsize)
        a = {title: self.page_no()-1}
        self.pagenumbers.update(a)
        h = self.fontsize * 0.9
        for i in self.data["songs"][title]["scheme"]:
            if self.get_y() + (self.data["songs"][title]["txt"][i].count("%") * self.fontsize * 0.65) >= 190 and self.renderchords:
                self.customfooter()
                self.add_page()
                h = self.data["songs"][title]["txt"][i].count(
                    "%") * self.fontsize * 0.6 + self.fontsize * 0.55
            elif self.get_y() + (len(self.multi_cell(0, 10, self.data["songs"][title]['txt'][i], 0, 'J', 0, True)) * self.fontsize * 0.35) > 130 and not self.renderchords:
                self.customfooter()
                self.add_page()
            self.multi_cell(
                0, self.fontsize*0.33, render_verse(self.data["songs"][title]["txt"][i], renderchords=self.renderchords))
            self.ln(self.sbv)
        print(f'sucsessfully added song "{title}" on page {self.page_no()-1}')

    def create_index(self):
        self.customfooter()
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


def import_song(inputfile: str = "tmp", title=""):
    with open(inputfile, 'r') as file:
        lines: list = file.readlines()
        txt: dict = {}
        verse: str = ""
        is_verse: bool = False
        song: dict = {"scheme": [], "txt": {}}
        for i, line in enumerate(lines):
            if line[0] == "&":
                title: str = line .replace("&", "").replace("\n", "")
            if line[0] == "+":
                song["scheme"] += [line .replace("+", "").replace("\n", "")]
            if is_verse is True and line[0] != "#":
                txt[verse] += [line .replace("\n", "")]
            if line[0] == "#":
                verse = line.replace("#", "").replace("\n", "")
                txt[verse] = []
                is_verse = True
        for g, h in txt.items():
            song["txt"][g] = ""
            for i in range(0, len(h), 2):
                c = []
                for line, k in enumerate(h[i]):
                    if not k == " ":
                        c += [(line, k)]

                song["txt"][g] += h[i+1][:c[0][0]]
                for line in range(len(c)):
                    song["txt"][g] += h[i+1][c[line - 1][0]
                        :c[line][0]] + "{" + c[line][1] + "}"
                song["txt"][g] += h[i+1][c[-1][0]:] + "%"
        for i in song["scheme"]:
            if i in song["txt"].keys():
                print(f"{Fore.GREEN}✓ checked {i}{Style.RESET_ALL}")
        with open("songs.json", "r") as f:
            data = json.load(f)
        if title in data.keys():
            if "y" == input(f"are you sure you want to repace {title} in songs.json [y/N]"):
                data["songs"][title] = song
            else:
                exit()
        else:
            data["songs"][title] = song
        rename("songs.json", f"backup/songs_old_{time()}.json")
        with open("songs.json", "a") as file:
            json.dump(data, file, sort_keys=True, ensure_ascii=False, indent=4)


def edit_song(song: dict):
    formatted: str = ""
    for verse in song["scheme"]:
        formatted += f"+{verse}\n"
    for verse, txt in song["txt"].items():
        formatted += f"#{verse}\n"
        formatted += render_verse(txt=txt)
    with open("tmp_edit", "w") as f:
        f.write(formatted)
    input("please edit the file tmp_edit to your liking and press enter")
    import_song("tmp_edit")


def remove_song():
    pass
