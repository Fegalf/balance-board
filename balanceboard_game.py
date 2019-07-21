# -*- coding: utf-8 -*-
import tkinter as tk
import os 
import pygame
import thorpy

application = thorpy.Application((340, 220), "Balance Board")

button_save_participant = thorpy.make_button("Créer participant")
button_calibration = thorpy.make_button('Calibration BOSU')
button_g0 = thorpy.make_button('Jeu #0')
button_g1 = thorpy.make_button('Jeu #1')
button_g2 = thorpy.make_button('Jeu #2')
tb = thorpy.make_text("Participant")

#set theme
thorpy.set_theme("human")
buttons = [button_save_participant, button_calibration, button_g0, button_g1, button_g2, tb]

#set default painter as ClassicFrame (same as used in theme 'classic')
thorpy.painterstyle.DEF_PAINTER = thorpy.painters.classicframe.ClassicFrame
thorpy.style.MARGINS = (50,2) #set default margins

background = thorpy.Background(image=thorpy.style.EXAMPLE_IMG, elements=buttons)
thorpy.store(background)

menu = thorpy.Menu([background])
menu.play()

application.quit()