import customtkinter
from PIL import Image, ImageTk

# https://gamebanana.com/tools/6934
# filename for all characters
characters_filename = [
    'mario', 'donkey', 'link', 'samus', 'samusd', 'yoshi', 'kirby', 'fox', 'pikachu', 'luigi', 'ness',
    'captain', 'purin', 'peach', 'daisy', ['koopa', 'koopag'], ['nana', 'popo'], 'sheik', 'zelda', 'mariod', # 'koopag' is gigabowser
    'pichu', 'falco', 'marth', 'lucina', 'younglink', 'ganon', 'mewtwo', 'roy', 'chrom', 'gamewatch', 'metaknight',
    'pit', 'pitb', 'szerosuit', 'wario', 'snake', 'ike', ['ptrainer', 'pzenigame', 'pfushigisou', 'plizardon'], # ptrainer pokemons
    'diddy', 'lucas', 'sonic', 'dedede', 'pikmin', 'lucario', 'robot', 'toonlink', 'wolf', 'murabito', 'rockman',
    'wiifit', 'rosetta', 'littlemac', 'gekkouga', 'palutena', 'pacman', #'miifighter', 'miiswordsman', 'miigunner' removed
    'reflet', 'shulk', 'koopajr', 'duckhunt', 'ryu', 'ken', 'cloud', 'kamui', 'bayonetta', 'inkling', 'ridley',
    'simon', 'richter', 'krool', 'shizue', 'gaogaen', 'packun', 'jack', 'brave', 'buddy', 'dolly', 'master',
    'tantan', 'pickel', 'edge', ['eflame', 'elight'], 'demon', 'trail' # 'element' for rex 
]

class CharacterSelectFrame(customtkinter.CTkFrame):
    def __init__(self, master, button_callback):
        super().__init__(master)

        # store callback function
        self.button_callback = button_callback

        # configure rows and columns
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1, uniform=1)

        # make grid of buttons for each character
        for i, character in enumerate(characters_filename):
            if type(character) is list:
                text = character[0]
            else:
                text = character

            try:
                image = customtkinter.CTkImage(Image.open(f"./icons/{text}.jpg"), size=(101, 58))
            except:
                print(f"{text} not found")
                pass
            
            # make button with character image
            button = customtkinter.CTkButton(self, text='', image=image, fg_color="transparent",
                                             border_spacing=0, corner_radius=0, border_width=0,
                                             command=lambda char=character: self.button_callback(char))

            #place button
            button.grid(row=i//12, column=i%12)

            # *when app is resized, images will not scale accordingly
            #  the button will scale if sticky="news" but image wont scale