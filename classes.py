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


class OpenButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(
            master=master,
            text=kwargs["fname"],
            fg_color=("#ACD400", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            border_color=("#ACD400", "#FE8A00"),
            border_width=5,
            text_color="black",
            command=lambda self=self: self.reset_frame(master),
        )

        self.place(relx=0.5, x=-620, y=100 + kwargs["row"] * 60)
        self.master = master
        self.file_name = kwargs["fname"]

        self.frame = Main_Frame(master=self.master, file_name=self.file_name)

        if self.file_name.rstrip(".csv") == kwargs["opened_frame"]:
            self.reset_frame(master)

    # returns command for reseting frame to main window
    def reset_frame(self, master):
        master.change_frame(exc=self.frame)

    # switches frame of buttons if its not an exception (exc = button that was pressed -> it will pack)
    def change_bframe(self, exc):
        if exc == self.frame:
            self.frame.f_pack()
        else:
            self.frame.self_forget()


# zbavit se tohohle
class Click_Button(ctk.CTkButton):
    def __init__(self, master, line, **kwargs):
        super().__init__(
            master=master,
            image=ctk.CTkImage(Image.open(f"Images/{line['image']}"), size=(160, 250)),
            compound="top",
            text=line["name"],
            fg_color=("#CEFE00", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            border_color=("#ACD400", "#FE8A00"),
            border_width=5,
            text_color="black",
            font=kwargs["font"],
            command=lambda self=self: web.open(line["web"]),
        )

        self.grid(row=kwargs["row"], column=kwargs["column"], pady=5, padx=2)


class Main_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.configure(width=900, height=900)

        self.f_pack()
        self.file_n = kwargs["file_name"]

        self.load_buttons()

    # forgets pack
    def self_forget(self):
        self.pack_forget()

    # pack
    def f_pack(self):
        self.pack(pady=50)

    # loads all buttons on the frame
    def load_buttons(self):
        _row, _column = 0, 0
        button_font = ctk.CTkFont(size=15, weight="bold")

        with open(f"Saves/{self.file_n}") as file:

            lines = csv.DictReader(file)

            for line in lines:
                button = Click_Button(
                    master=self, line=line, font=button_font, row=_row, column=_column
                )
                print(line)
                _column += 1
                if _column == 5:
                    _column = 0
                    _row += 1
