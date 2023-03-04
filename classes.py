import customtkinter as ctk
from PIL import Image
import webbrowser as web
import csv


class AddWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Add Webbie2")
        self.geometry("500x400+600+300")

        image_button = ctk.CTkButton(self, width=160, height=250)
        image_button.grid(row=0, column=0, rowspan=3, padx=20, pady=20)

        name_label = ctk.CTkLabel(self, text="Add Window")
        name_label.grid(row=0, column=1, padx=20, pady=20)

        name_entry = ctk.CTkEntry(self, placeholder_text="Webbie2", state="normal")
        name_entry.grid(row=0, column=2, padx=20, pady=20)

        web_label = ctk.CTkLabel(self, text="Web link")
        web_label.grid(row=1, column=1, padx=20, pady=20)

        web_entry = ctk.CTkEntry(self, placeholder_text="https://www.google.cz/")
        web_entry.grid(row=1, column=2, padx=20, pady=20)

        add_button = ctk.CTkButton(self, text="Done")
        add_button.grid(row=2, column=2, padx=20, pady=20)


class FileButton(ctk.CTkButton):
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

    def frame_change(self):
        self.master.change_frame(self.name)


class Main_Frame(ctk.CTkScrollableFrame):
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

        with open(f"Saves/{self.name}") as file:

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


# this button opens saved web links
class WebButton(ctk.CTkButton):
    def __init__(self, **kwargs):
        super().__init__(
            master=kwargs["master"],
            image=ctk.CTkImage(
                Image.open(f"Images/{kwargs['line']['image']}"), size=(160, 250)
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

    def open_web(self):
        web.open(self.weblink)
