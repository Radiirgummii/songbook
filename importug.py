import json
from colorama import Fore, Style

with open("tmp", 'r') as f:
    a = f.readlines()
    b = {}
    l = 0
    s = False
    song = {"scheme": [], "txt": {}}
    for i, j in enumerate(a):
        if j[0] == "+":
            song["scheme"] += [j.replace("+", "").replace("\n", "")]
        if s is True and j[0] != "#":
            b[l] += [j.replace("\n", "")]
        if j[0] == "#":
            l = j.replace("#", "").replace("\n", "")
            b[l] = []
            s = True
    for g, h in b.items():
        song["txt"][g] = ""
        for i in range(0, len(h), 2):
            c = []
            for j, k in enumerate(h[i]):
                if not k == " ":
                    c += [(j, k)]

            song["txt"][g] += h[i+1][:c[0][0]]
            for j in range(len(c)):
                song["txt"][g] += h[i+1][c[j-1][0]
                    :c[j][0]] + "{" + c[j][1] + "}"
            song["txt"][g] += h[i+1][c[-1][0]:] + "\n"
    for i in song["scheme"]:
        if i in song["txt"].keys():
            print(f"{Fore.GREEN}✓ checked {i}{Style.RESET_ALL}")
    with open("tmp.json", "a") as file:
        json.dump(song, file)
        print(song["txt"]["s1"])

