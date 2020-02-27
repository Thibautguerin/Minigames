#!/usr/bin/python3

import sys
sys.path.insert(0, '../include')
from include import *

def _render_region(image, rect, color, rad):
    corners = rect.inflate(-2*rad, -2*rad)
    for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
        pygame.draw.circle(image, color, getattr(corners,attribute), rad)
    image.fill(color, rect.inflate(-2*rad,0))
    image.fill(color, rect.inflate(0,-2*rad))

def displayRect(surface, rect, color, rad=0, aa=True, border=0, inside=(0,0,0)):
    if (aa == True):
        rect = pygame.Rect(rect)
        _aa_render_region(surface, rect, color, rad)
        if (border):
            rect.inflate_ip(-2*border, -2*border)
            _aa_render_region(surface, rect, inside, rad)
    else:
        rect = pygame.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0,0
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill((0,0,0,0))
        _render_region(image, zeroed_rect, color, rad)
        if (border):
            zeroed_rect.inflate_ip(-2*border, -2*border)
            _render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)


def _aa_render_region(image, rect, color, rad):
    corners = rect.inflate(-2*rad-1, -2*rad-1)
    for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
        x, y = getattr(corners, attribute)
        gfxdraw.aacircle(image, x, y, rad, color)
        gfxdraw.filled_circle(image, x, y, rad, color)
    image.fill(color, rect.inflate(-2*rad,0))
    image.fill(color, rect.inflate(0,-2*rad))
