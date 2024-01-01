from Basics import *

class Tile():
    def __init__(self, colors : list, values : list, board):
        self.colors = colors[randint(0, len(colors)-1)]
        if self.colors == ["wild"]:
            self.colors += board.game.config.pallette
        self.value = values[randint(0, len(values)-1)]
        self.board = board
        self.render()

    def render(self):
        self.image = pygame.Surface((6*self.board.game.config.scaleX, 6*self.board.game.config.scaleY))
        if self.colors[0] == "wild":
            self.image.fill(self.board.game.config.colortable[self.colors[0]])
        if len(self.colors) == 1:
            self.image.fill(self.board.game.config.colortable[self.colors[0]])
        elif len(self.colors) == 2:
            self.image.fill(self.board.game.config.colortable[self.colors[0]])
            pygame.draw.rect(self.image, self.board.game.config.colortable[self.colors[1]], (3*self.board.game.config.scaleX, 0, ceil(3*self.board.game.config.scaleX), ceil(6*self.board.game.config.scaleY)))
        if self.value != 0:
            num = self.board.game.config.Write(3, str(self.value))
            self.image.blit(num, (3*self.board.game.config.scaleX-num.get_width()/2, 3*self.board.game.config.scaleY-num.get_height()/2))


    def match(self):
        self.board.game.score += self.value
        return True