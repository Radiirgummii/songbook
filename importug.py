import json
from colorama import Fore, Style #type: ignore
from os import rename

with open("tmp", 'r') as file:
    lines:list = file.readlines()
    txt: dict = {}
    verse:str = ""
    is_verse: bool = False
    song: dict = {"scheme": [], "txt": {}}
    for i, line in enumerate(lines):
        if line[0] == "+":
            song["scheme"] += [line .replace("+", "").replace("\n", "")]
        if is_verse is True and line [0] != "#":
            txt[verse] += [line .replace("\n", "")]
        if line[0] == "#":
            verse = line.replace("#", "").replace("\n", "")
            txt[verse] = []
            is_verse = True
    for g, h in txt.items():
        song["txt"][g] = ""
        for i in range(0, len(h), 2):
            c = []
            for line , k in enumerate(h[i]):
                if not k == " ":
                    c += [(line , k)]

            song["txt"][g] += h[i+1][:c[0][0]]
            for line  in range(len(c)):
                song["txt"][g] += h[i+1][c[line -1][0]
                    :c[line ][0]] + "{" + c[line ][1] + "}"
            song["txt"][g] += h[i+1][c[-1][0]:] + "\n"
    for i in song["scheme"]:
        if i in song["txt"].keys():
            print(f"{Fore.GREEN}✓ checked {i}{Style.RESET_ALL}")
    rename("tmp.json", "tmp.json.old")
    with open("tmp.json", "a") as file:
        json.dump(song, file,sort_keys=True)

