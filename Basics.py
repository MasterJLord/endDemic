import pygame, random, sys, math, json
from random import randint
from pygame.locals import *
# from dataclasses import dataclass
from math import floor, ceil, sin, cos

def toDict(filename: str):
    """This converts a filename into the contained hashmap."""
    return json.loads(open(filename+".json").read())


# @dataclass
class setup():
    def __init__(self):
        self.boardSize = [8, 10]
        self.colors = [["yellow"], ["blue"], ["greenblue"], ["gray"], ["salmon"], ["green"], ["yellow"], ["blue"], ["greenblue"], ["gray"], ["salmon"], ["green"], ["yellow"], ["blue"], ["greenblue"], ["gray"], ["salmon"], ["green"], ["yellow"], ["blue"], ["greenblue"], ["gray"], ["salmon"], ["green"], ["yellow"], ["blue"], ["greenblue"], ["gray"], ["salmon"], ["green"], ["salmon", "yellow"], ["greenblue", "blue"], ["gray", "green"], ["wild"]]
        self.pallette = ["yellow", "blue", "greenblue", "salmon", "green"]
        self.colortable = {
            "red": (180, 40, 40),
            "yellow": (170, 170, 40),
            "salmon": (190, 110, 100),
            "gray": (130, 130, 130),
            "green": (80, 160, 80),
            "greenblue": (60, 160, 160),
            "blue": (40, 40, 180),
            "wild": (200, 220, 220)
        }
        self.startingTileValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2]
        self.scaleX = 1
        self.scaleY = 1
        self.boardTop = 0
        self.phase = "matching"
        self.FontResolution = 12
        self.TextColor = (255, 255, 255)
        self.DefaultFont = []
        self.LetterHeight = 0



    def Write(self, size: float, writing: str, maxwidth: int = None, overflow: bool = True, color: tuple = None):
        # Defaults the text color to the default text color
        if color == None:
            color = self.TextColor
        # Renders text in a single line
        if maxwidth == None:
            text = self.DefaultFont.render(str(writing), True, color)
            height = 1
        # Renders multiple lines of text
        else:
            widths = {}
            for c in str(writing):
                widths[self.DefaultFont.render(c, True, color)] = c
            maxwidth = maxwidth*self.scaleX * \
                self.LetterHeight/(size*self.scaleY)
            length = 0
            if overflow:
                rows = [""]
                for c in widths.items():
                    length += c[0].get_width()
                    if length >= maxwidth:
                        length = c[0].get_width()
                        rows.append(c[1])
                    else:
                        rows[len(rows)-1] = rows[len(rows)-1]+c[1]
                height = len(rows)
                imagerows = []
                for s in rows:
                    imagerows.append(self.DefaultFont.render(s, True, color))
                text = pygame.Surface(
                    (maxwidth, self.LetterHeight*height), pygame.SRCALPHA)
                for r in range(height):
                    text.blit(imagerows[r], (0, (r)*self.LetterHeight))
            else:
                row = ""
                for c in widths.items():
                    length += c[0].get_width()
                    if length >= maxwidth:
                        break
                    else:
                        row = row+c[1]
                text = self.DefaultFont.render(row, True, color)
                height = 1
        # Scales text to size parameter and returns it
        XToYRatio = text.get_width()/(self.LetterHeight)
        return pygame.transform.scale(text, (math.ceil(size*self.scaleY*XToYRatio), math.ceil(size*self.scaleY*height)))





class Game():
    def __init__(self):
        self.board = []
        self.config = setup()
        self.score = 0
        self.scoreThreshold = 30
        self.timer = 0
        self.timeLimit = 90000
        self.stacks = []
        self.plants = toDict("Plants")
        self.phase = "winning"
        self.artifactList = toDict("Artifacts")
        self.choices = []
        self.inventory = []



# for (c, v) in pygame.color.THECOLORS.items():
#     print(c)