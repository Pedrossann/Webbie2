import customtkinter as ctk
import csv
from PIL import Image
import os
import classes


# Main App ______________________________________________________________________
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1300x800+100+100")
        self.title("Webbie2")

        self.list_of_files = []
        self.list_of_frames = []
        self.list_of_widgets = []
        self.button_remove = False
        self.set_colours()

        bg_image = ctk.CTkImage(
            Image.open("Webbie2/BuildedImages/background.png"), size=(1920, 1080)
        )

        background = ctk.CTkLabel(master=self, image=bg_image, text="")
        background.place(relx=0.5, x=-(self.winfo_screenwidth() / 2))
        self.list_of_widgets.append({"Main_frame_bg": background})
        self.create_main_frame()
        self.create_menubox()

    # reset main frame
    def reset_main_frame(self):

        self.list_of_files = []

        for frame in self.list_of_frames:
            frame.self_forget()

        self.list_of_frames = []

        self.create_main_frame()

    # create main frame
    def create_main_frame(self):

        files = os.listdir(os.getcwd() + "\Webbie2\Saves")

        for file in files:

            self.list_of_files.append(
                classes.FrameButton(
                    master=self,
                    text=os.path.splitext(file)[0],
                    row=len(self.list_of_files),
                )
            )
            self.list_of_frames.append(classes.MainFrame(master=self, file=file))
        self.list_of_widgets.append({"Frame_buttons": self.list_of_files})

        self.last_settings()

        # top menu box ________________________________________________________

    def create_menubox(self):
        frame_menu_box = ctk.CTkFrame(master=self, height=40, width=500)
        frame_menu_box.place(x=15, y=5)
        self.list_of_widgets.append({"Menu_box_frame": frame_menu_box})

        self.add_button = ctk.CTkButton(
            master=frame_menu_box,
            text="Add",
            width=20,
            fg_color=(self.light_fg_colour, self.dark_fg_colour),
            hover_color=(self.light_hoover_colour, self.dark_hoover_colour),
            border_color=(self.light_fg_colour, self.dark_fg_colour),
            border_width=5,
            text_color="black",
            command=self.open_add_window,
        )
        self.add_button.place(x=120, y=5)

        self.remove_button = ctk.CTkButton(
            master=frame_menu_box,
            text="Remove",
            width=20,
            fg_color=(self.light_fg_colour, self.dark_fg_colour),
            hover_color=(self.light_hoover_colour, self.dark_hoover_colour),
            text_color="black",
            border_width=5,
            border_color=(self.light_fg_colour, self.dark_fg_colour),
            command=self.click_remove_button,
        )
        self.remove_button.place(x=180, y=5)

        switch_mode_button = ctk.CTkSwitch(
            master=frame_menu_box,
            text="Mode",
            command=self.mode_switch,
            fg_color=(self.light_fg_colour, self.dark_fg_colour),
        )

        switch_mode_button.place(
            x=15, y=5,
        )

    def click_remove_button(self):
        if self.button_remove == False:
            self.remove_button.configure(border_color="red")
            self.button_remove = True

        else:
            self.remove_button.configure(
                border_color=(self.light_bg_colour, self.dark_bg_colour)
            )
            self.button_remove = False

    # check saved settings from last running and recreates last app setting
    def last_settings(self):
        with open("Webbie2/last_settings.csv") as file:
            lines = csv.reader(file)
            for line in lines:

                # open last dark/light mode
                if line[0] == "Dark":
                    ctk.set_appearance_mode("Dark")
                else:
                    ctk.set_appearance_mode("Light")
                # open last frame
                for frame in self.list_of_frames:
                    if os.path.splitext(frame.name)[0] == line[1]:
                        frame.pack(pady=50)
                        self.opened_frame = os.path.splitext(frame.name)[0]

    # set colours
    def set_colours(self):
        with open("Webbie2/last_settings.csv") as file:
            lines = csv.reader(file)
            for line in lines:

                # setting colours
                self.light_fg_colour = line[2]
                self.light_bg_colour = line[3]
                self.dark_fg_colour = line[4]
                self.dark_bg_colour = line[5]
                self.light_hoover_colour = line[6]
                self.dark_hoover_colour = line[7]

    # changes app mode
    def mode_switch(self):
        if ctk.get_appearance_mode() == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

        self.save()

    # creates new window crom classes file
    def open_add_window(self):

        add_window = classes.AddWindow(self)
        add_window.grab_set()

    # saves changes to csv file
    def save(self):
        with open("Webbie2/last_settings.csv", "w") as file:
            line = csv.writer(file, lineterminator="")
            line.writerow(
                [
                    ctk.get_appearance_mode(),
                    os.path.splitext(self.opened_frame)[0],
                    self.light_fg_colour,
                    self.light_bg_colour,
                    self.dark_fg_colour,
                    self.dark_bg_colour,
                    self.light_hoover_colour,
                    self.dark_hoover_colour,
                ]
            )

    # switches between frames
    def change_frame(self, open):
        for frame in self.list_of_frames:
            if os.path.splitext(frame.name)[0] == open:
                frame.pack(pady=50)
                self.opened_frame = os.path.splitext(frame.name)[0]
            else:
                frame.self_forget()
        self.save()


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
