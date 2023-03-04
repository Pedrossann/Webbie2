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

        bg_image = ctk.CTkImage(
            Image.open("Webbie2/BuildedImages/background.png"), size=(1920, 1080)
        )

        background = ctk.CTkLabel(master=self, image=bg_image, text="")
        background.place(relx=0.5, x=-(self.winfo_screenwidth() / 2))
        self.list_of_widgets.append({"Main_frame_bg": background})

        files = os.listdir(os.getcwd() + "\Webbie2\Saves")

        for file in files:
            self.list_of_files.append(
                classes.FrameButton(
                    master=self, text=file.rstrip(".csv"), row=len(self.list_of_files)
                )
            )
            self.list_of_frames.append(classes.MainFrame(master=self, file=file))
        self.list_of_widgets.append({"Frame_buttons": self.list_of_files})

        self.last_settings()

        # top menu box ________________________________________________________
        frame_menu_box = ctk.CTkFrame(master=self, height=40, width=500)
        frame_menu_box.place(x=15, y=5)
        self.list_of_widgets.append({"Menu_box_frame": frame_menu_box})

        self.add_button = ctk.CTkButton(
            master=frame_menu_box,
            text="Add",
            width=20,
            fg_color=("#ACD400", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            text_color="black",
            command=self.open_add_window,
        )
        self.add_button.place(x=120, y=5)

        self.remove_button = ctk.CTkButton(
            master=frame_menu_box,
            text="Remove",
            width=20,
            fg_color=("#ACD400", "#FE8A00"),
            hover_color=("#BAE500", "#FE6C00"),
            text_color="black",
        )
        self.remove_button.place(x=180, y=5)

        switch_mode_button = ctk.CTkSwitch(
            master=frame_menu_box, text="Mode", command=self.mode_switch
        )
        switch_mode_button.place(
            x=15, y=5,
        )

    # check saved settings from last running and recreates last app setting
    def last_settings(self):
        with open("Webbie2/last_opened.csv") as file:
            lines = csv.reader(file)
            for line in lines:
                if line[0] == "Dark":
                    ctk.set_appearance_mode("Dark")
                else:
                    ctk.set_appearance_mode("Light")
                for frame in self.list_of_frames:
                    if frame.name.rstrip(".csv") == line[1]:
                        frame.pack(pady=50)
                        self.opened_frame = frame.name.rstrip(".csv")

    # changes app mode
    def mode_switch(self):
        if ctk.get_appearance_mode() == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

        self.save()

    # creates new window crom classes file
    def open_add_window(self):

        add_window = classes.AddWindow()
        add_window.grab_set()

    # saves changes to csv file
    def save(self):
        with open("last_opened.csv", "w") as file:
            line = csv.writer(file, lineterminator="")
            line.writerow([ctk.get_appearance_mode(), self.opened_frame.rstrip(".csv")])

    # switches between frames
    def change_frame(self, open):
        for frame in self.list_of_frames:
            if frame.name.rstrip(".csv") == open:
                frame.pack(pady=50)
                self.opened_frame = frame.name.rstrip(".csv")
            else:
                frame.self_forget()
        self.save()


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
