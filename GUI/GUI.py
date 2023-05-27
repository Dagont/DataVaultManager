import tkinter as tk
import customtkinter as ctk

import GUI_FrameOne
import GUI_FrameTwo
import GUI_FrameThree
import GUI_FrameFour

from GUI_FrameFour import FrameFour

ctk.set_appearance_mode("dark")


class DataVaultManagerApp(ctk.CTk):
    """
    A Tkinter application for managing DataVault 2.0.
    """

    def __init__(self):
        super().__init__()

        # Window settings
        self.title("DataVault 2.0 Manager")
        self.minsize(600, 500)

        # Fonts
        self.regular = ctk.CTkFont(family="Roboto", size=14)
        self.subtle = ctk.CTkFont(family="Roboto", size=10)

        # File path
        self.file_path = None

        # Frames
        self.frames = {}
        self.frame_order = [
            'FrameOne',
            'FrameTwo',
            'FrameThree'
        ]
        self.current_frame = 'FrameOne'
        self.frame_history = []

        self.create_widgets()

    def create_widgets(self):
        """
        Creates frames for the application and navigation buttons for each frame.
        """
        for Frame in [GUI_FrameOne.FrameOne, GUI_FrameTwo.FrameTwo, GUI_FrameThree.FrameThree]:
            frame_id = Frame.__name__
            frame = Frame(app=self, master=self)
            self.frames[frame_id] = frame
            frame.pack(side="top", fill="both", expand=True)
            frame.pack_forget()

            # Add "Back" and "Next" button to each frame
            self.create_nav_buttons(frame)

        self.show_frame(self.current_frame)

    def create_frame_four_instances(self, count, entities):
        for i, entity in enumerate(entities):
            frame_id = f"FrameFour_{i}"
            print(f"Creating {frame_id}")
            frame = FrameFour(app=self, master=self, entity=entity)
            self.frames[frame_id] = frame

            frame.pack(side="top", fill="both", expand=True)
            frame.pack_forget()
            self.create_nav_buttons(frame)
            # Add FrameFour to frame_order
            self.frame_order.append(frame_id)
            print(f"Frame order: {self.frame_order}")

        #self.show_frame(f"FrameFour_{0}")


    def create_nav_buttons(self, frame):
        """
        Creates 'Back' and 'Next' navigation buttons for a given frame.
        """
        back_button = ctk.CTkButton(master=frame, text="Back", command=self.go_back, width=50)
        back_button.pack(side="left", anchor="sw", padx=10, pady=10)

        next_button = ctk.CTkButton(master=frame, text="Next", command=self.go_next, width=50)
        next_button.pack(side="right", anchor="se", padx=10, pady=10)

    def go_back(self):
        """
        Switches the display to the previous frame in the history.
        """
        if len(self.frame_history) <= 1:
            return
        self.hide_current_frame()
        self.frame_history.pop()
        previous_index = self.frame_order.index(self.current_frame) - 1
        self.current_frame = self.frame_order[previous_index]
        self.show_frame(self.current_frame)


        #self.current_frame = self.frame_history.pop()
        #self.show_frame(self.current_frame)

    def go_next(self):
        """
        Switches the display to the next frame in the order.
        """
        current_frame = self.frames[self.current_frame]
        if hasattr(current_frame, "process_data"):
            current_frame.process_data()

        current_index = self.frame_order.index(self.current_frame)

        if current_index + 1 < len(self.frame_order):
            next_frame = self.frame_order[current_index + 1]
            self.show_frame(next_frame)

    def hide_current_frame(self):
        """
        Hides the currently displayed frame.
        """
        current_frame = self.frames[self.current_frame]
        current_frame.pack_forget()

    def show_frame(self, frame_id):
        """
        Displays a frame given its identifier.
        """
        self.hide_current_frame()

        self.frame_history.append(self.current_frame)

        self.current_frame = frame_id
        frame = self.frames[frame_id]
        frame.pack(side="top", fill="both", expand=True)


if __name__ == "__main__":
    app = DataVaultManagerApp()
    app.mainloop()
