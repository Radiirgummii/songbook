from songbook import SONGBOOK
import json


def main():
    with open("songs.json", 'r') as f:
        data = json.load(f)
    songbook = SONGBOOK(form="A5", index="all with testing",
                        fontsize=9, rimg=False, data=data)
    songbook.build_songbook()
    songbook.output('songbook.pdf', 'F')


if __name__ == "__main__":
    main()
