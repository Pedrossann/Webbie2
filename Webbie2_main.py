import customtkinter as ctk
import webbrowser as web
import os
import csv
from PIL import Image


############################# App #############################
# creates the main window, which then creates buttons and opens last opened file
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1300x800+100+100")
        self.title("Webbie2")

        self.openbutton = []
        files_list = os.listdir(os.getcwd() + "\Saves")
        bg_image = ctk.CTkImage(
            Image.open("BuildedImages/background.png"), size=(1920, 1080)
        )

        self.add_window = None
        with open("last_opened.csv") as file:
            lines = csv.reader(file)
            for line in lines:
                if line[0] == "Dark":
                    ctk.set_appearance_mode("Dark")
                else:
                    ctk.set_appearance_mode("Light")
                opened_frame = line[1]

        background = ctk.CTkLabel(self, image=bg_image, text="")
        background.place(relx=0.5, x=-(self.winfo_screenwidth() / 2))

        frame_menu_box = ctk.CTkFrame(master=self, height=40, width=500)
        frame_menu_box.place(x=15, y=5)

        switch_mode_button = ctk.CTkSwitch(
            master=frame_menu_box,
            text="Mode",
            command=lambda self=self: self.mode_switch(),
        )
        switch_mode_button.place(
            x=15, y=5,
        )

        add_button = AddButton(frame_menu_box, window=self)
        remove_button = RemoveButton(frame_menu_box)

        for file in files_list:
            self.openbutton.append(
                OpenButton(
                    self,
                    fname=file,
                    row=len(self.openbutton),
                    opened_frame=opened_frame,
                )
            )

    # sends signal to all the frames witch checks if they should be open or not (all except exc will forgot pack)
    def change_frame(self, exc):
        for button in self.openbutton:
            button.change_bframe(exc)
        self.opened = exc.file_n
        self.save()

    # change mode and saves the change into the file
    def mode_switch(self):
        if ctk.get_appearance_mode() == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
        self.save()

    def save(self):
        with open("last_opened.csv", "w") as file:
            line = csv.writer(file, lineterminator="")
            line.writerow([ctk.get_appearance_mode(), self.opened.rstrip(".csv")])

    def open_window(self):
        if self.add_window == None:
            self.add_window = AddWindow(self)
            self.add_window.focus()
        else:
            self.add_window.focus()

    def app_update(self):
        if self.add_window:
            self.add_window.focus()


class AddButton(ctk.CTkButton):
    def __init__(self, master, window):
        super().__init__(
            master=master,
            text="Add",
            width=20,
            fg_color=("#ACD400", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            text_color="black",
            command=lambda self=self: window.open_window(),
        )

        self.place(x=120, y=5)


class AddWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        label = ctk.CTkLabel(self, text="Add Window")
        label.pack()


class RemoveButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(
            master=master,
            text="Remove",
            width=20,
            fg_color=("#ACD400", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            text_color="black",
        )

        self.place(x=180, y=5)


# Button for opening frame ___________________________________
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


# Frame with opened grid of buttons of separate web browsers
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
                _column += 1
                if _column == 5:
                    _column = 0
                    _row += 1


# Final button that opens the web _______________________________________
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


def main():
    app = App()
    while True:
        app.app_update()
        app.update()


if __name__ == "__main__":
    main()
