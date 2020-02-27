#!/usr/bin/python3

import sys
sys.path.insert(0, '../include')
from include import *

def wait_mouse_up():
	x = 1

	while (x == 1):
		for event in pygame.event.get():
			if (event.type == MOUSEBUTTONUP):
				x = 0
				break
		clockFps.tick(maxFps)

def wait_key_up():
	x = 1

	while (x == 1):
		for event in pygame.event.get():
			if (event.type == KEYUP):
				x = 0
				break
		clockFps.tick(maxFps)