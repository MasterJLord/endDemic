from Tiles import *

class Board():
    def __init__(self, game):
        self.board = []
        self.game = game
        self.fill()


    def fill(self):
        self.board = []
        for i in range(self.game.config.boardSize[1]):
            self.board.append([])
            for j in range(self.game.config.boardSize[0]):
                self.board[i].append(Tile(self.game.config.colors, self.game.config.startingTileValues, self))
        tempAllList = []
        for i in range(self.game.config.boardSize[1]):
            for j in range(self.game.config.boardSize[0]):
                tempAllList.append((j, i))
        tempAllMatches = self.checkMatches(tempAllList)
        while tempAllMatches != []:
            for m in tempAllMatches:
                if m[1] == "horizontal":
                    for i in range(m[4]):
                        self.board[m[3]][m[2]+i] = Tile(self.game.config.colors, self.game.config.startingTileValues, self)
                elif m[1] == "vertical":
                    for i in range(m[4]):
                        self.board[m[3]+i][m[2]] = Tile(self.game.config.colors, self.game.config.startingTileValues, self)
            tempAllMatches = self.checkMatches(tempAllList)



    def checkMatches(self, tiles : tuple):
        matches = []        
        for t in tiles:
            for c in self.board[t[1]][t[0]].colors:
                matches.append(self.horizontals(t, c))
                matches.append(self.verticals(t, c))
        while None in matches:
            matches.remove(None)
        return matches


    def horizontals(self, tile : tuple, color : str):
        left = 1
        right = 1
        while tile[0]-left >= 0 and color in self.board[tile[1]][tile[0]-left].colors:
            left += 1
        while tile[0]+right < self.game.config.boardSize[0] and color in self.board[tile[1]][tile[0]+right].colors:
            right += 1
        
        left -= 1
        right -= 1

        if left+right >= 2:
            return (color, "horizontal", tile[0]-left, tile[1], left+right+1)
        

    def verticals(self, tile : tuple, color : str):
        above = 1
        below = 1

        while tile[1]-above >= 0 and color in self.board[tile[1]-above][tile[0]].colors:
            above += 1
        while tile[1]+below < self.game.config.boardSize[1] and color in self.board[tile[1]+below][tile[0]].colors:
            below += 1
        
        above -= 1
        below -= 1

        if above+below >= 2:
            return (color, "vertical", tile[0], tile[1]-above, above+below+1)
    


    def cleanup(self, matches : list):
            for m in matches:
                if m[1] == "horizontal":
                    for i in range(m[4]):
                        if self.board[m[3]][m[2]+i] != None:
                            self.board[m[3]][m[2]+i].match()
                            self.board[m[3]][m[2]+i] = None
                elif m[1] == "vertical":
                    for i in range(m[4]):
                        if self.board[m[3]+i][m[2]] != None:
                            self.board[m[3]+i][m[2]].match()
                            self.board[m[3]+i][m[2]] = None



    def settle(self):
        settled = False
        for x in range(self.game.config.boardSize[0]):
            for y in reversed(range(self.game.config.boardSize[1])):
                if self.board[y][x] == None:
                    settled = True
                    if y == 0:
                        self.board[y][x] = Tile(self.game.config.colors, self.game.config.startingTileValues, self)
                    else:
                        self.board[y][x] = self.board[y-1][x]
                        self.board[y-1][x] = None
        if settled:
            return False
        else:
            tempAllList = []
            for i in range(self.game.config.boardSize[1]):
                for j in range(self.game.config.boardSize[0]):
                    tempAllList.append((j, i))
            tempAllMatches = self.checkMatches(tempAllList)
            if tempAllMatches == []:
                return True
            else:
                self.cleanup(tempAllMatches)
