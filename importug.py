with open("tmp", 'r') as f:
    a = f.readlines()
    b = []
    for j, i in zip(a, range(0, len(a))):
        b += [j.replace("\n", "")]
    for i in range(0, len(b)-1, 2):
        c = []
        for j, k in enumerate(b[i]):
            if not k == " ":
                c += [(j, k)]
        print(b[i+1][:c[0][0]], end="")
        for j in range(len(c)):
            print(b[i+1][c[j-1][0]:c[j][0]] +
                  "{" + c[j][1] + "}", end="")
        print(b[i+1][c[-1][0]:], end="%")
