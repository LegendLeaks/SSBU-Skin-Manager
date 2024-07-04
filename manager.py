import os
import shutil
import time

characters = [
    "Mario", "Donkey Kong", "Link", "Samus", "Dark Samus", "Yoshi", "Kirby", "Fox", "Pikachu",
    "Luigi", "Ness", "Captain Falcon", "Jigglypuff", "Peach", "Daisy", "Bowser", "Ice Climbers",
    "Sheik", "Zelda", "Dr. Mario", "Pichu", "Falco", "Marth", "Lucina", "Young Link", "Ganondorf",
    "Mewtwo", "Roy", "Chrom", "Mr. Game & Watch", "Meta Knight", "Pit", "Dark Pit", "Zero Suit Samus",
    "Wario", "Snake", "Ike", "PKMN Trainer", "Diddy Kong", "Lucas", "Sonic", "King Dedede", "Olimar",
    "Lucario", "R.O.B.", "Toon Link", "Wolf", "Villager", "Mega Man", "Wii Fit Trainer",
    "Rosalina & Luma", "Little Mac", "Greninja", "Palutena", "Pacman", "Robin", "Shulk", "Bowser Jr.",
    "Duck Hunt", "Ryu", "Ken", "Cloud", "Corrin", "Bayonetta", "Inkling", "Ridley", "Simon", "Richter",
    "King K. Rool", "Isabelle", "Incineroar", "Piranha Plant", "Joker", "Hero", "Banjo & Kazooie",
    "Terry", "Byleth", "Min Min", "Steve", "Sephiroth", "Pyra/Mythra", "Kazuya", "Sora"
]

class Manager:
    def __init__(self):
        pass
        
    def startup(self):
        # if new skins in inactive skins folder, move it to respective folder
        pass

    def swap_skins(app, active_skin, inactive_skin):
        # move inactive skin to mods folder
        if inactive_skin != 'default':
            shutil.move(os.path.join(app.inactive_skins_folder, app.character, inactive_skin), app.mods_folder)

        # move active skins to skin storage folder
        if active_skin != 'default':
            shutil.move(os.path.join(app.mods_folder, active_skin), os.path.join(app.inactive_skins_folder, app.character))
    
    def get_skins(app):
        '''
        gets all inactive skins for a given character
        '''

        if app.character is None or app.inactive_skins_folder is None:
            return
        
        path = os.path.join(app.inactive_skins_folder, app.character)

        # list of lists to store skins for each skin slot
        skins = [[] for _ in range(8)]

        for skin in os.listdir(path):
            # first get skin id
            skin_id = app.get_skin_ids(os.path.join(path, skin))[0]
            skins[skin_id].append(skin)
        
        return skins

    def get_active_skins(app):
        '''
        gets all active skins for a given character
        sorted by slots 00-07
        '''
        active_skins = ['default' for _ in range(8)]
        for index, skin in enumerate(os.listdir(os.path.join(app.mods_folder))):
            print(skin)
            try:
                skin_ids = app.get_skin_ids(os.path.join(app.mods_folder, skin))
                skin_id = skin_ids[0] #take first one for now, add multi slot compatability later
                active_skins[skin_id] = skin
            except:
                continue
        print(active_skins)
        return active_skins
    
    def get_skin_ids(app, skin_filepath):
        
        skin_ids = os.listdir(os.path.join(skin_filepath, 'fighter', app.character, 'model', 'body'))
        
        # convert from 'c02' to 2
        for i, v in enumerate(skin_ids):
            skin_ids[i] = int(skin_ids[i][2])

        return skin_ids # returns list of skin ids

    def generate_skin_folders(app):
        '''
        generates skin storage folders for each character
        '''
        if app.inactive_skins_folder is None:
            return

        # generate folders
        for char in characters:

            if type(char) is list:
                char = char[0]
            
            # make a folder for each character if it doesnt already exist
            path = os.path.join(app.inactive_skins_folder, char)

            if os.path.exists(path):
                continue
            else:
                os.makedirs(path)

    def separate_skins(app, path):
        # INCOMPLETE

        # this function splits multi-slot skins into separate skins
        # path --> path to skin folder 

        skin_ids = app.get_skin_ids(path)

        for i, skin_id in enumerate(skin_ids):
            #   duplicate folder
            new_dir = path.split('/')[-1]
            new_dir += '_c0' + str(skin_ids[i])
            new_dir = os.path.join(app.inactive_skins_folder, app.character, new_dir)
            #new_dir = self.inactive_skins_folder + '/' + self.character + '/' + new_dir

            shutil.copytree(path, new_dir)
            print('folder duplicated to ' + new_dir)

            #   cleaning up ui folder:

            # delete chara3 and chara7
            ui_path = (os.path.join(new_dir, 'ui', 'replace', 'chara'))
            print(ui_path)
            try:
                shutil.rmtree(os.path.join(ui_path, 'chara_3'))
                shutil.rmtree(os.path.join(ui_path, 'chara_7'))
            except OSError as error:
                print(error)

            # delete unneeded files from chara0 - chara6
            for folder in os.listdir(ui_path):
                for file in os.listdir(os.path.join(ui_path, folder)):
                    if '0'+str(skin_id) in str(file):
                        continue
                    os.remove(os.path.join(ui_path, folder, file))
            print('ui folder cleaned up')

            #   cleaning up fighter folders
            fighter_path = os.path.join(new_dir, 'fighter', app.character, 'model')

            for model in os.listdir(fighter_path):
                for folder in os.listdir(os.path.join(fighter_path, model)):
                    if folder == 'c0'+str(skin_id):
                        continue
                    shutil.rmtree(os.path.join(fighter_path, model, folder))
            print('fighter folder cleaned up')

            #   cleaning up sound folders
            sound_path = os.path.join(new_dir, 'sound', 'bank', 'fighter_voice')

            for file in os.listdir(sound_path):
                if 'c0'+str(skin_id) in file:
                    continue
                os.remove(os.path.join(sound_path, file))
            
            print('sound folders cleaned up')



            

# debugging code
# x = Manager()

# x.character = 'inkling'
# x.inactive_skins_folder = 'C:\\Users\\vsvan\\Desktop\\Smash_Skins'
# x.separate_skins('C:\\Users\\vsvan\\Downloads\\extracto_temp\\Octoling_Main')
