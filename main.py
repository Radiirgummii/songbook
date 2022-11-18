from songbook import SONGBOOK, import_song, edit_song, remove_song
import json


def main():
    while True:
        options: str = '''
g  = Generate new songbook
s  = edit/add song
i  = edit/add index
q  = quit
        '''
        print(options)
        choice: str = input()
        if choice.lower() == "g":
            generate_songbook_menu()
        elif choice.lower() == "s":
            song_menu()
        elif choice.lower() == "i":
            index_menu()
        elif choice.lower() == "q":
            break
        else:
            print("command not specified")


def song_menu():
    options = '''
a  = add song
e  = edit song
r  = remove song
q  = quit to main menu
    '''
    while True:
        print(options)
        choice: str = input()
        if choice.lower() == "a":
            import_song(input("inputfile: "), input("Title: "))
            break
        elif choice.lower() == "e":
            with open(input("datafile: "), "r") as f:
                song = json.load(f)["songs"][input("song: ")]
                edit_song(song)
            break
        elif choice.lower() == "r":
            remove_song()
            break
        elif choice.lower() == "q":
            break
        else:
            print("command not defined")


def index_menu():
    pass


def generate_songbook_menu() -> None:
    with open("songs.json", 'r') as f:
        data = json.load(f)
        songbook = SONGBOOK(form="A5", index="testing",
                            fontsize=9, renderimg=False, data=data)
        songbook.build_songbook()
        songbook.output('songbook.pdf', 'F')


if __name__ == "__main__":
    main()
