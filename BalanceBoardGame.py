# -*- coding: utf-8 -*-
import tkinter as tk
import multiprocessing as mp 
import pygame
from calibration import run_calibration
import os 

class BalanceBoardGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.mw = master
        self.mw.protocol("WM_DELETE_WINDOW", self.mw.destroy)

        self.mw.title("Balance Board Game")
        self.mw.geometry("340x220")
        self.mw.resizable(0, 0)
        self.create_widgets()
        self.path_to_data = None
        self.participant = None

    def create_widgets(self):
        label_participant = tk.Label(self.mw, text="Participant :")
        label_participant.place(x=20, y=18)
        self.entry = tk.Entry(self.mw, textvariable=tk.StringVar(), width=30)
        self.entry.place(x=90, y=20)

        self.button_save_participant = tk.Button(self.mw, text='Créer', command=self.create_participant_folder_and_enable_calibration)
        self.button_save_participant.place(x=280, y=16)

        self.button_calibration = tk.Button(self.mw, text='Calibration BOSU', state='disabled', command=self.run_calibration)
        self.button_calibration.pack()
        self.button_g0 = tk.Button(self.mw, text='Jeu #0', state='disabled', command=self.run_game_0)
        self.button_g0.pack()
        self.button_g1 = tk.Button(self.mw, text='Jeu #1', state='disabled', command=self.run_game_1)
        self.button_g1.pack()
        self.button_g2 = tk.Button(self.mw, text='Jeu #2', state='disabled', command=self.run_game_2)
        self.button_g2.pack()
        self.mw.update()

        self.mw_center = self.mw.winfo_width() // 2

        self.button_calibration.place(x=self.mw_center - self.button_calibration.winfo_width()//2, y=55)
        self.button_g0.place(x=self.mw_center - self.button_g0.winfo_width()//2, y=95)
        self.button_g1.place(x=self.mw_center - self.button_g1.winfo_width()//2, y=135)
        self.button_g2.place(x=self.mw_center - self.button_g2.winfo_width()//2, y=175)

    def run_calibration(self):
        self.calibration = run_calibration()
        self.activate_widget(self.button_g0)
        self.activate_widget(self.button_g1)
        self.activate_widget(self.button_g2)

    def run_game_0(self,):
        from level_0 import level_0
        level_0(self.path_to_data, self.calibration)
        pygame.quit()
    
    def run_game_1(self):
        from level_1 import level_1
        level_1(self.path_to_data, self.calibration)
        pygame.quit()

    def run_game_2(self):
        from level_2 import level_2
        level_2(self.path_to_data, self.calibration)
        pygame.quit()

    def create_participant_folder_and_enable_calibration(self):
        """Create participant data folder if it does not already exist."""
        if  self.entry.get() != '':
            self.path_to_data = os.path.join(os.getcwd(), 'Data', self.entry.get())
            self.disable_widget(self.entry)
            self.disable_widget(self.button_save_participant)
            self.activate_widget(self.button_calibration)
            try:
                os.mkdir(self.path_to_data)
                for i in range(3):
                    os.mkdir(os.path.join(self.path_to_data, 'jeu{}'.format(i)))
            except FileExistsError:
                pass

    def disable_widget(self, widget):
        widget['state'] = 'disabled'

    def activate_widget(self, widget):
        widget['state'] = 'active'

if __name__=="__main__":
    root = tk.Tk()
    bbg = BalanceBoardGame(root)
    bbg.mainloop()
    import sys; sys.quit()
