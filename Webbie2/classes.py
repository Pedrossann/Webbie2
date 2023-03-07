import customtkinter as ctk
from PIL import Image
import webbrowser as web
import csv


# add window opens new TopLevel window in which we can create new web opening button(WebButton)
class AddWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Add Webbie2")
        self.geometry("500x400+600+300")

        self.choose_frame_create()

    def choose_frame_create(self):
        self.addbutton_window_create()
        self.addfolder_window_create()

        self.choose_frame = ctk.CTkFrame(self)
        self.choose_frame.pack()

        button_frame = ctk.CTkButton(
            self.choose_frame,
            text="Add Button",
            width=160,
            height=250,
            fg_color=("#CEFE00", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            border_color=("#ACD400", "#FE8A00"),
            border_width=5,
            text_color="black",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.addbutton_place,
        )
        button_frame.grid(row=0, column=0)

        choose_folder_frame = ctk.CTkButton(
            self.choose_frame,
            text="Add Folder",
            width=160,
            height=250,
            fg_color=("#CEFE00", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            border_color=("#ACD400", "#FE8A00"),
            border_width=5,
            text_color="black",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.addfolder_window_place,
        )
        choose_folder_frame.grid(row=0, column=1)

    def addbutton_place(self):
        self.choose_frame.forget()
        self.button_frame.pack()

    def addfolder_window_place(self):
        self.choose_frame.forget()
        self.folder_frame.pack()

    def addfolder_window_create(self):
        self.folder_frame = ctk.CTkFrame(self)

        add_folder_entry = ctk.CTkEntry(self.folder_frame)
        add_folder_entry.pack()

        add_folder_button = ctk.CTkButton(self.folder_frame, text="Done")
        add_folder_button.pack()

    def addbutton_window_create(self):

        self.button_frame = ctk.CTkFrame(self)

        image_button = ctk.CTkButton(
            master=self.button_frame,
            width=160,
            height=250,
            text="Click to choose",
            fg_color=("#CEFE00", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            border_color=("#ACD400", "#FE8A00"),
            border_width=5,
            text_color="black",
            font=ctk.CTkFont(size=15, weight="bold"),
        )

        image_button.grid(row=0, column=0, rowspan=3, padx=20, pady=20)

        name_label = ctk.CTkLabel(self.button_frame, text="Name")
        name_label.grid(row=0, column=1, padx=20, pady=20)

        name_entry = ctk.CTkEntry(
            self.button_frame, placeholder_text="Webbie2", state="normal"
        )
        name_entry.grid(row=0, column=2, padx=20, pady=20)

        web_label = ctk.CTkLabel(self.button_frame, text="Web link")
        web_label.grid(row=1, column=1, padx=20, pady=20)

        web_entry = ctk.CTkEntry(
            self.button_frame, placeholder_text="https://www.google.cz/"
        )
        web_entry.grid(row=1, column=2, padx=20, pady=20)

        add_button = ctk.CTkButton(
            master=self.button_frame,
            text="Done",
            fg_color=("#CEFE00", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            border_color=("#ACD400", "#FE8A00"),
            border_width=5,
            text_color="black",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        add_button.grid(row=2, column=2, padx=20, pady=20)


# this Button switches between MainFrames
class FrameButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(
            master=master,
            text=kwargs["text"],
            fg_color=("#ACD400", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            border_color=("#ACD400", "#FE8A00"),
            border_width=5,
            text_color="black",
            command=self.frame_change,
        )

        self.place(relx=0.5, x=-620, y=100 + kwargs["row"] * 60)

        self.master = master
        self.name = kwargs["text"]

    # switches the frame
    def frame_change(self):
        self.master.change_frame(self.name)


# MainFrame contains all the web opening buttons (WebButton). All of those frames are created at the start of the app and then thez switch bz fressing FrameButtons
class MainFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=900, height=900)

        self.name = kwargs["file"]
        self.list_of_buttons = []

        self.create_buttons()
        self.grid_buttons()

    def self_forget(self):
        self.pack_forget()

    # creates all the buttons from the file
    def create_buttons(self):

        with open(f"Webbie2/Saves/{self.name}") as file:

            lines = csv.DictReader(file)

            for line in lines:
                self.list_of_buttons.append(WebButton(master=self, line=line))

    # places all created buttons on the frame
    def grid_buttons(self):
        row, column = 0, 0
        for button in self.list_of_buttons:

            button.grid(row=row, column=column, pady=5, padx=2)
            column += 1
            if column == 6:
                column = 0
                row += 1


# This button opens saved web links
class WebButton(ctk.CTkButton):
    def __init__(self, **kwargs):
        super().__init__(
            master=kwargs["master"],
            image=ctk.CTkImage(
                Image.open(f"Webbie2/Images/{kwargs['line']['image']}"), size=(160, 250)
            ),
            compound="top",
            text=kwargs["line"]["name"],
            fg_color=("#CEFE00", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            border_color=("#ACD400", "#FE8A00"),
            border_width=5,
            text_color="black",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.open_web,
        )
        self.weblink = kwargs["line"]["web"]

    # this function opens saved weblink
    def open_web(self):
        web.open(self.weblink)
