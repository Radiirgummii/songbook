import json as json
#Functions
def render_chord(txt):
    a = txt.split("%")
    b = []
    ftxt = ""

    #split lines seperated by %
    for z,i in zip(a, range(len(a))):
        b.append([])
        x = []
        a = z.split("}")
        for j in a:
            x.append(j.split("{"))
        b[i].extend(x)
        a = []
        for i in b:
            c = ""
            d = ""
            for j in i:
                
                
                if len(j) == 1:
                    d += j[0]
                else:
                    c += " " * len(j[0]) + j[1]
                    d += j[0]
        ftxt += c
        if c != "":
            ftxt += "\n"
        ftxt += d
        ftxt += "\n"





    return ftxt


#reading Data
with open("songs.json", 'r') as f:
  data = json.load(f)
lol = [data[0]["txt"]["s1"], data[0]["txt"]["s2"]]
for i in lol:
    print(render_chord(i))