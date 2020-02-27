#!/usr/bin/python3

from math import *
from random import *
import re
import os
import contextlib
with contextlib.redirect_stdout(None):
	import pygame
	import pygame.gfxdraw
	from pygame import *
import time
import threading
import random
import sqlite3

# SQL

sql_users = """CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				pseudo TEXT NOT NULL,
				password TEXT NOT NULL
			);"""

connection = sqlite3.connect("./save/profiles/users.db")
cursor = connection.cursor()

cursor.execute(sql_users)

PLAYER = 0

# PROFILES

global_profile = 0

# GAMES

sologame = 0

# CRYPT

#KEY = AES.new("43UHFIULY937Y83HD839YODI3YH8DYLO83YD83TD74IGDI37TD78", AES.MODE_CFB)

# RESOLUTION

pygame.init()

infoObject = pygame.display.Info()
res_tab = [(infoObject.current_w, infoObject.current_h), (1920, 1080), (1600, 900), (1280, 720), (960, 540)]
int_res = 0
mult = 1.0
resolution = (1920, 1080)

pygame.quit()

# FPS

clockFps = pygame.time.Clock()
fps_tab = [30, 60, 120, 144]
int_fps = 0
maxFps = 30
fpsAnim = 50

# LANGUAGE

FRENCH = {
	"play":"Jouer",
	"param":"Paramètres",
	"res":"Résolution",
	"lang":"Français",
	"fs":"Plein Écran",
	"fps":"Ips",
	"by":"Par",
	"gamemode":"Modes de jeu",
	"solo":"Solo",
	"multi":"Multijoueur",
	"profiles":"Profils",
	"profile":"Profil",
	"bad_pswd":"Mot de passe incorrect!",
	"new_usr":"Nouvel utilisateur",
	"delete_usr":"Supprimer l'utilisateur",
	"delete_usr?":"Voulez vous supprimer cet utilisateur définitivement?",
	"yes":"Oui",
	"no":"Non",
	"no_usr":"Pas d'utilisateurs!",
	"create_usr":"Création d'un utilisateur",
	"create":"Créer",
	"pseudo":"Pseudo",
	"password":"Mot de passe",
	"verif_password":"Vérification du mot de passe",
	"bad_form":"Veuillez remplir tous les champs!",
	"bad_verif_password":"Vérification du mot de passe invalide!",
	"quit_prog":"Souhaitez vous quitter Minigames?",
	"background":"Fond d'écran",
	"writing_color":"Couleur du texte",
	"default":"Défaut",
	"multicolour":"Multicolore"
}

ENGLISH = {
	"play":"Play",
	"param":"Settings",
	"res":"Resolution",
	"lang":"English",
	"fs":"Fullscreen",
	"fps":"Fps",
	"by":"By",
	"gamemode":"Game modes",
	"solo":"Solo",
	"multi":"Multiplayer",
	"profiles":"Profiles",
	"profile":"Profile",
	"bad_pswd":"Bad password!",
	"new_usr":"New user",
	"delete_usr":"Delete the user",
	"delete_usr?":"Do you want to permanently delete this user?",
	"yes":"Yes",
	"no":"No",
	"no_usr":"No users!",
	"create_usr":"Creation of a user",
	"create":"Create",
	"pseudo":"Pseudo",
	"password":"Password",
	"verif_password":"Verify the password",
	"bad_form":"Please complete all fields!",
	"bad_verif_password":"Invalid password check!",
	"quit_prog":"Do you want to leave Minigames?",
	"background":"Background color",
	"writing_color":"Text color",
	"default":"Default",
	"multicolour":"Multicolour"
}

SPANISH = {
	"play":"Jugar",
	"param":"Configuraciones",
	"res":"Resolución",
	"lang":"Español",
	"fs":"Pantalla Completa",
	"fps":"Fps",
	"by":"Por",
	"gamemode":"Modos de juego",
	"solo":"Solo",
	"multi":"Multijugador",
	"profiles":"Perfiles",
	"profile":"Perfil",
	"bad_pswd":"¡Contraseña incorrecta!",
	"new_usr":"Nuevo usuario",
	"delete_usr":"Borrar el usuario",
	"delete_usr?":"¿Quieres eliminar de forma permanente este usuario?",
	"yes":"Sí",
	"no":"No",
	"no_usr":"¡No hay usuarios!",
	"create_usr":"Creación de un usuario",
	"create":"Crear",
	"pseudo":"Apodo",
	"password":"Contraseña",
	"verif_password":"Verificación de la contraseña",
	"bad_form":"Por favor, rellene todos los campos!",
	"bad_verif_password":"Verificación de contraseña inválida",
	"quit_prog":"¿Te gustaría dejar Minigames?",
	"background":"Fondo",
	"writing_color":"Color de texto",
	"default":"Defecto",
	"multicolour":"multicolor"
}

GERMAN = {
	"play":"Spielen",
	"param":"Einstellungen",
	"res":"Bildschirmauflösung",
	"lang":"Deutsch",
	"fs":"Vollbildschirm",
	"fps":"Bps",
	"by":"Durch",
	"gamemode":"Spielmodi",
	"solo":"Solo",
	"multi":"Multiplayer",
	"profiles":"Benutzerprofil",
	"profile":"Benutzerprofil",
	"bad_pswd":"Falsches passwort!",
	"new_usr":"Neuer benutzer",
	"delete_usr":"Löschen sie den benutzer",
	"delete_usr?":"Möchten Sie diesen Benutzer dauerhaft löschen?",
	"yes":"Ja",
	"no":"Nein",
	"no_usr":"Keine benutzer!",
	"create_usr":"Erstellung eines Benutzer",
	"create":"Schaffen",
	"pseudo":"Spitzname",
	"password":"Passwort",
	"verif_password":"Passwortüberprüfung",
	"bad_form":"Veuillez remplir tous les champs!",
	"bad_verif_password":"Bitte füllen sie alle felder aus!",
	"quit_prog":"Würden Sie Minigames verlassen?",
	"background":"Hintergrund",
	"writing_color":"Textfarbe",
	"default":"Standard",
	"multicolour":"Mehrfarben"
}

lang_tab = [FRENCH, ENGLISH, SPANISH, GERMAN]
int_lang = 0
LANG = FRENCH

# COLOR

background = (30, 30, 30)
write_color = (255, 255, 255)
button_color = (81, 137, 173)
button_on_click_color = (236, 216, 87)
param_color = (50, 50, 50)
param_on_click_color = (100, 100, 100)

alpha_load = 0
alpha_profile = 255
aa_load = False
rainbow_b = False
rainbow_w = False

# READ SETTINGS

def read_settings():
	global resolution
	global int_res
	global mult

	global maxFps
	global int_fps

	global LANG
	global int_lang

	global background
	global write_color
	global button_color
	global button_on_click_color
	global param_color
	global param_on_click_color

	global rainbow_b
	global rainbow_w

	i = 0

	if (os.path.isfile(".settings") is True):
		file = open(".settings", "r")
		data = file.read()
		tab = data.split('\n')
		while (i != len(tab)):
			tab[i] = tab[i].split(';')
			i = i + 1
		resolution = (int(tab[0][0]), int(tab[0][1]))
		int_res = int(tab[1][0])
		mult = float(tab[2][0])
		maxFps = int(tab[3][0])
		int_fps = int(tab[4][0])
		int_lang = int(tab[5][0])
		LANG = lang_tab[int_lang]
		background = (int(tab[6][0]), int(tab[6][1]), int(tab[6][2]))
		write_color = (int(tab[7][0]), int(tab[7][1]), int(tab[7][2]))
		button_color = (int(tab[8][0]), int(tab[8][1]), int(tab[8][2]))
		button_on_click_color = (int(tab[9][0]), int(tab[9][1]), int(tab[9][2]))
		param_color = (int(tab[10][0]), int(tab[10][1]), int(tab[10][2]))
		param_on_click_color = (int(tab[11][0]), int(tab[11][1]), int(tab[11][2]))
		if (tab[12][0] == "True"):
			rainbow_b = True
		else:
			rainbow_b = False
		if (tab[13][0] == "True"):
			rainbow_w = True
		else:
			rainbow_w = False

read_settings()