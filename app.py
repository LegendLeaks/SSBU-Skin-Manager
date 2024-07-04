import customtkinter
from PIL import Image, ImageTk
from customtkinter import filedialog
import manager
from manager import Manager, characters
from CharacterSelectFrame import CharacterSelectFrame, characters_filename

# *put homepage in a seperate Frame class
#  put manager page in a seperate Frame class
#  keep this file only for making instances of other classes

class RadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values, selected=''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value=selected) # which button is selected by default

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", font=("verdana", 18), corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable, font=("verdana", 14),)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(5, 5), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # instance of Manager class
        self.man = Manager()

        # app title and size
        self.title("Ultimate Skin Manager by LegendLeakz")
        self.geometry("1280x720+320+120")
        self.minsize(1280, 720)
        self.maxsize(1920, 1080)
        self.skins_page = 1
        self.current_page = 'homepage'

        # configure columns and rows based on page
        self.grid_columnconfigure((1, 2, 3, 4), weight=4)
        self.grid_columnconfigure((0, 5), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        # for activating 'select character' button
        self.folder_selected = False
        self.inactive_skins_folder = None
        self.yuzu_folder = None
        self.mods_folder = None
        self.character = None

        # ----- HOME PAGE -----

        # Create main title
        self.home_title = customtkinter.CTkLabel(self, text='Ultimate Skin Manager', font=("Impact", 80))

        # Create buttons
        self.btn_select = customtkinter.CTkButton(self, text="Select Character", width = 500, height = 50,
                                                  font = ("Verdana", 20), state='disabled', command=self.btn_select_char_callback)
        self.btn_skins_folder = customtkinter.CTkButton(self, text="Change Skins Folder", width = 500, height = 50,
                                                        font = ("Verdana", 20), command=self.btn_folder1_callback)
        self.btn_yuzu_folder = customtkinter.CTkButton(self, text="Change Yuzu Folder", width = 500, height = 50,
                                                       font = ("Verdana", 20), command=self.btn_folder2_callback)

        # ----- MANAGER PAGE -----

        # create character title label
        self.char_title = customtkinter.CTkLabel(self, text="Character", font=("Verdana", 60))

        #   create buttons
        # update
        self.btn_update = customtkinter.CTkButton(self, text="UPDATE SKINS", width = 500, height = 50, 
                                                  font = ("Verdana", 20), command=self.btn_update_callback)
        # next page
        img_nextpage = customtkinter.CTkImage(Image.open("./images/next_arrow.png"), size=(40, 40))
        self.btn_nextpage = customtkinter.CTkButton(self, image=img_nextpage, text='', width=40, height=40,
                                                       command=self.btn_page2_callback)
        # previous page
        img_prevpage = customtkinter.CTkImage(Image.open("./images/prev_arrow.png"), size=(40, 40))
        self.btn_prevpage = customtkinter.CTkButton(self, image=img_prevpage, text='', width=40, height=40,
                                                       command=self.btn_page1_callback)
        # back to homepage
        self.btn_homepage = customtkinter.CTkButton(self, image=img_prevpage, text='', width=30, height=30,
                                                    command=self.btn_return_homepage_callback)
        
        self.show_homepage()
    
    # callback function for character selection class
    def char_selected(self, char):
        # this function is called when a character is selected

        print(f"{char} selected")

        # update character title
        char_index = characters_filename.index(char)
        character = characters[char_index]
        if type(character) is list:
            character = character[0]
        self.char_title.configure(text=character)

        # update character in Manager class
        self.character = char

        # hide char select frame, show skin manager frame
        self.selection_frame.grid_forget()
        self.show_managerpage()
    
    def setModsFolder(self):
        # yuzu_folder is set to '' if 'cancel' is pressed during folder selection
        if self.yuzu_folder != '':
            self.mods_folder = self.yuzu_folder + '/sdmc/ultimate/mods'
            print(self.mods_folder)

    def hide_homepage(self):
        # hide homepage elements
        self.home_title.grid_forget()
        self.btn_select.grid_forget()
        self.btn_skins_folder.grid_forget()
        self.btn_yuzu_folder.grid_forget()

    def show_homepage(self):
        # show homepage elements
        self.home_title.grid(row=0, column=1, pady=(50, 10), sticky="nesw", columnspan=4)
        self.btn_select.grid(row=2, column=1, padx = (300, 300), columnspan=4)
        self.btn_skins_folder.grid(row=3, column=1, padx = (300, 300), columnspan=4)
        self.btn_yuzu_folder.grid(row=4, column=1, padx = (300, 300), columnspan=4)

    def hide_managerpage(self):
        # hide manager elements
        self.hide_page1()
        self.hide_page2()

        self.char_title.grid_forget()
        self.btn_update.grid_forget()
        self.btn_nextpage.grid_forget()
        self.btn_prevpage.grid_forget()
        self.btn_homepage.grid_forget()
    
    def generate_button_values(self):
        # add inactive skins to skins list
        skins = manager.get_skins(self)

        # add default skin option
        for slot in skins:
            slot.insert(0, 'default')
        
        # add active skins to selected list
        selected = manager.get_skins(self)
        print(selected)

        # add active skins to skins list
        for i, slot in enumerate(skins):
            if selected[i] != 'default':
                slot.append(selected[i])
        
        return skins, selected
        

    def show_managerpage(self):
        # generate radiobuttons for each skin slot
        button_values, selected = self.generate_button_values()

        self.radio_frame1 = RadiobuttonFrame(self, "Slot 1", values=button_values[0], selected=selected[0])
        self.radio_frame2 = RadiobuttonFrame(self, "Slot 2", values=button_values[1], selected=selected[1])
        self.radio_frame3 = RadiobuttonFrame(self, "Slot 3", values=button_values[2], selected=selected[2])
        self.radio_frame4 = RadiobuttonFrame(self, "Slot 4", values=button_values[3], selected=selected[3])
        self.radio_frame5 = RadiobuttonFrame(self, "Slot 5", values=button_values[4], selected=selected[4])
        self.radio_frame6 = RadiobuttonFrame(self, "Slot 6", values=button_values[5], selected=selected[5])
        self.radio_frame7 = RadiobuttonFrame(self, "Slot 7", values=button_values[6], selected=selected[6])
        self.radio_frame8 = RadiobuttonFrame(self, "Slot 8", values=button_values[7], selected=selected[7])

        # show manager elements
        self.show_page1()
        self.char_title.grid(row=0, column=1, padx=(10, 10), pady=(20, 10), sticky = "ns", columnspan=4)
        self.btn_update.grid(row=4, column=1, columnspan=4)
        self.btn_nextpage.grid(row=1, column = 5, padx = (0, 20), rowspan=3, sticky="w")
        self.btn_prevpage.grid(row=1, column = 0, padx = (20, 0), rowspan=3, sticky="e")
        self.btn_homepage.grid(row=0, column=0, padx=(40, 0), pady=(40, 0), sticky="nw")
    
    def hide_page1(self):
        self.radio_frame1.grid_forget()
        self.radio_frame2.grid_forget()
        self.radio_frame3.grid_forget()
        self.radio_frame4.grid_forget()
    
    def show_page1(self):
        self.radio_frame1.grid(row=1, column=1, padx=(10, 10), rowspan=3, sticky="nsew")
        self.radio_frame2.grid(row=1, column=2, padx=(10, 10), rowspan=3, sticky="nsew")
        self.radio_frame3.grid(row=1, column=3, padx=(10, 10), rowspan=3, sticky="nsew")
        self.radio_frame4.grid(row=1, column=4, padx=(10, 10), rowspan=3, sticky="nsew")
    
    def hide_page2(self):
        self.radio_frame5.grid_forget()
        self.radio_frame6.grid_forget()
        self.radio_frame7.grid_forget()
        self.radio_frame8.grid_forget()
    
    def show_page2(self):
        self.radio_frame5.grid(row=1, column=1, padx=(10, 10), pady=(10, 0), rowspan=3, sticky="nsew")
        self.radio_frame6.grid(row=1, column=2, padx=(10, 10), pady=(10, 0), rowspan=3, sticky="nsew")
        self.radio_frame7.grid(row=1, column=3, padx=(10, 10), pady=(10, 0), rowspan=3, sticky="nsew")
        self.radio_frame8.grid(row=1, column=4, padx=(10, 10), pady=(10, 0), rowspan=3, sticky="nsew")
    
    def btn_page2_callback(self):
        if self.skins_page != 2:
            self.hide_page1()
            self.show_page2()

            self.skins_page = 2

    def btn_page1_callback(self):
        if self.skins_page != 1:
            self.hide_page2()
            self.show_page1()

            self.skins_page = 1
    
    def btn_select_char_callback(self):
        self.hide_homepage()
        # create char selection frame
        self.selection_frame = CharacterSelectFrame(self, self.char_selected)
        self.selection_frame.grid(row=0, column=0)
    
    def btn_return_homepage_callback(self):
        self.hide_managerpage()
        self.show_homepage()

    def btn_update_callback(self):
        # get all skins user wants active
        updated_skins = []
        updated_skins.append(self.radio_frame1.get())
        updated_skins.append(self.radio_frame2.get())
        updated_skins.append(self.radio_frame3.get())
        updated_skins.append(self.radio_frame4.get())
        updated_skins.append(self.radio_frame5.get())
        updated_skins.append(self.radio_frame6.get())
        updated_skins.append(self.radio_frame7.get())
        updated_skins.append(self.radio_frame8.get())

        # get current active skins
        active_skins = manager.get_active_skins(app)

        for i in range(8):
            if updated_skins[i] == active_skins[i]:
                continue
            # swap skins
            manager.swap_skins(self, active_skins[i], updated_skins[i])

        #self.selectfile()
    
    def btn_folder1_callback(self):
        self.inactive_skins_folder = self.selectfolder()
        print(self.inactive_skins_folder)

        # enable 'select character' button
        if self.folder_selected:
            self.btn_select.configure(state='normal')
        self.folder_selected = True
    
    def btn_folder2_callback(self):
        self.yuzu_folder = self.selectfolder()
        self.setModsFolder()

        # enable 'select character' button
        if self.folder_selected:
            self.btn_select.configure(state='normal')
        self.folder_selected = True
    
    def selectfolder(self):
        #filename = filedialog.askopenfilename()
        folder_path = filedialog.askdirectory()
        return folder_path

app = App()
app.mainloop()