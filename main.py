from Stacks import *
from Board  import *

pygame.init()

clock = pygame.time.Clock()

display = pygame.display.set_mode((0, 0))
screen = pygame.Surface((display.get_width(), display.get_height()), pygame.SRCALPHA)

game = Game()


game.config.scaleX = screen.get_width()/100
game.config.scaleY = screen.get_height()/100
game.config.boardTop = (98-game.config.boardSize[1]*7)*game.config.scaleY
game.config.DefaultFont = pygame.font.SysFont("moderno20", int(screen.get_height()*game.config.FontResolution/100))
game.config.LetterHeight = game.config.DefaultFont.render("fj", True, game.config.TextColor).get_height()

for c in game.config.pallette:
    possibilities = []
    for s in range(len(game.plants[0])):
        if game.plants[0][s][0] == c:
            possibilities.append(s)
    game.stacks.append(Stack(game, c, game.plants[0].pop(possibilities[randint(0, len(possibilities)-1)])[1:]))


game.board = Board(game)

game.phase = "matching"


swaps = []
waitFrame = 11


while True:
    mouseClicks = [(-1, -1)]
    thisFrameTime = clock.tick(60)
    for X in pygame.event.get():
        if X.type == pygame.QUIT or (X.type == pygame.KEYDOWN and X.key == pygame.K_ESCAPE):
            sys.exit()

        elif X.type == pygame.MOUSEBUTTONDOWN:
            mouseClicks.insert(0, pygame.mouse.get_pos())
            if game.phase == "matching" and len(swaps) in {0, 1}:
                swaps.append((floor(mouseClicks[0][0]/(7*game.config.scaleX)), floor((mouseClicks[0][1]-game.config.boardTop)/(7*game.config.scaleY))))
                if swaps[0][0] < 0 or swaps[0][0] >= game.config.boardSize[0] or swaps[0][1] < 0 or swaps[0][1] >= game.config.boardSize[1]:
                    swaps.pop(len(swaps)-1)
                elif len(swaps) == 2 and not ((swaps[1][1]-swaps[0][1] in {-1, 1} and swaps[1][0]-swaps[0][0] == 0) or (swaps[1][0]-swaps[0][0] in {-1, 1} and swaps[1][1]-swaps[0][1] == 0)):
                    swaps = []
            elif game.phase == "artifactChoice":
                if mouseClicks[0][1] < 50*game.config.scaleY:
                    game.inventory.append(game.choices[0])
                    game.phase = "equip"
                else:
                    game.inventory.append(game.choices[1])
                    game.phase = "equip"
                for s in game.stacks:
                    s.setup()

            elif game.phase == "equip":
                print(floor(mouseClicks[0][1]/(100*game.config.scaleY/len(game.stacks))))
                game.stacks[floor(mouseClicks[0][1]/(100*game.config.scaleY/len(game.stacks)))].artifacts.append(Artifact(game, game.inventory.pop(0)))
                for s in game.stacks:
                    s.setup()
                game.scoreThreshold = ceil(game.scoreThreshold*1.3)
                game.score = 0
                game.timeLimit = 60000
                game.timer = 0
                game.board.fill()
                game.phase = "matching"
                # waitFrame = 10
                # game.phase = "starting"



        elif X.type == pygame.MOUSEBUTTONUP:
            mouseClicks.insert(0, pygame.mouse.get_pos())
            if game.phase == "matching" and len(swaps) == 1:
                swaps.append((floor(mouseClicks[0][0]/(7*game.config.scaleX)), floor((mouseClicks[0][1]-game.config.boardTop)/(7*game.config.scaleY))))
                if swaps[1][0] < 0 or swaps[1][0] >= game.config.boardSize[0] or swaps[1][1] < 0 or swaps[1][1] >= game.config.boardSize[1]:
                    swaps.pop(1)
                elif swaps[0] == swaps[1]:
                    swaps.pop(1)
                elif not ((swaps[1][1]-swaps[0][1] in {-1, 1} and swaps[1][0]-swaps[0][0] == 0) or (swaps[1][0]-swaps[0][0] in {-1, 1} and swaps[1][1] - swaps[0][1] == 0)):
                    swaps = []


    if game.phase == "matching":
        game.timer += thisFrameTime
        if len(swaps) == 2:
            temp = game.board.board[swaps[0][1]][swaps[0][0]]
            game.board.board[swaps[0][1]][swaps[0][0]] = game.board.board[swaps[1][1]][swaps[1][0]]
            game.board.board[swaps[1][1]][swaps[1][0]] = temp
            swaps.append(-1)
            waitFrame = 5
        elif len(swaps) == 3:
            waitFrame -= 1
            if waitFrame == 0:
                matches = game.board.checkMatches(swaps[0:2])
                if matches == []:
                    temp = game.board.board[swaps[1][1]][swaps[1][0]]
                    game.board.board[swaps[1][1]][swaps[1][0]] = game.board.board[swaps[0][1]][swaps[0][0]]
                    game.board.board[swaps[0][1]][swaps[0][0]] = temp
                else:
                    for s in game.stacks:
                        s.trigger(matches)
                    game.board.cleanup(matches)
                    game.phase = "falling"
                    waitFrame = 3
                swaps = []
        if game.timer > game.timeLimit and game.phase == "matching":
            sys.exit()
        
        
    elif game.phase == "falling":
        game.timer += thisFrameTime/2
        if waitFrame == 0:
            if game.board.settle():
                game.phase = "matching"
            else:
                waitFrame = 3
        else:
            waitFrame -= 1

    # if game.phase == "starting":
    #     if waitFrame == 30:
    #         game.phase = "matching"
    #     else:
    #         waitFrame += 1
    #     print(waitFrame)
    
    # if game.phase == "winning":
    #     if waitFrame == 30:
    #         game.phase = "artifacts"
        
    #     else:
    #         waitFrame += 1
    #     print(waitFrame)

    
    if game.phase == "artifactChoice":
        screen.fill((0, 0, 0))
        topChoice = game.config.Write(8, game.choices[0] + ": " + game.artifactList[game.choices[0]], 80)
        screen.blit(topChoice, (50*game.config.scaleX-topChoice.get_width()/2, 25*game.config.scaleY-topChoice.get_height()/2))
        bottomChoice = game.config.Write(8, game.choices[1] + ": " + game.artifactList[game.choices[1]], 80)
        screen.blit(bottomChoice, (50*game.config.scaleX-bottomChoice.get_width()/2, 75*game.config.scaleY-bottomChoice.get_height()/2))

    if game.phase == "equip":
        for s in range(len(game.stacks)):
            pygame.draw.rect(screen, game.config.colortable[game.stacks[s].type], (0, s*100/len(game.stacks)*game.config.scaleY, 100*game.config.scaleX, 100*game.config.scaleY))
            for b in range(len(game.stacks[s].stack)):
                screen.blit(game.stacks[s].stack[b].image, ((4+7*b)*game.config.scaleX, s*100/len(game.stacks)*game.config.scaleY+1*game.config.scaleY))


    if game.phase == "matching" or game.phase == "falling":
        # if game.score >= game.scoreThreshold:
        if game.score >= game.scoreThreshold:
            game.phase = "artifactChoice"
            game.choices = [randint(0, len(game.artifactList.keys())-1), randint(0, len(game.artifactList.keys())-1)]
            if game.choices[1] == game.choices[0]:
                game.choices[1] -= 1
            game.choices[0] = list(game.artifactList.keys())[game.choices[0]]
            game.choices[1] = list(game.artifactList.keys())[game.choices[1]]
            waitFrame = 0

        screen.fill((0, 0, 0))
        if (len(swaps) == 1): 
            pygame.draw.rect(screen, (70, 70, 10), (swaps[0][0]*7*game.config.scaleX, swaps[0][1]*7*game.config.scaleY+game.config.boardTop, 7*game.config.scaleX, 7*game.config.scaleY))
        for i in range(game.config.boardSize[1]):
            for j in range(game.config.boardSize[0]):
                if game.board.board[i][j] != None:
                    screen.blit(game.board.board[i][j].image, ((j*7+0.5)*game.config.scaleX, (i*7+0.5)*game.config.scaleY+game.config.boardTop))

        for s in range(len(game.stacks)):
            pygame.draw.rect(screen, game.config.colortable[game.stacks[s].type], ((7*game.config.boardSize[0]+2)*game.config.scaleX, s*100/len(game.stacks)*game.config.scaleY, 100*game.config.scaleX, 100*game.config.scaleY))
            for b in range(len(game.stacks[s].pool)):
                screen.blit(game.stacks[s].pool[b].image, ((7*game.config.boardSize[0]+4)*game.config.scaleX+7*b*game.config.scaleX, s*100/len(game.stacks)*game.config.scaleY+1*game.config.scaleY))
            for b in range(len(game.stacks[s].stack)):
                screen.blit(game.stacks[s].stack[b].image, ((7*game.config.boardSize[0]+8)*game.config.scaleX+7*len(game.stacks[s].pool)*game.config.scaleX+7*b*game.config.scaleX, s*100/len(game.stacks)*game.config.scaleY+1*game.config.scaleY))
                    
        scoreText = game.config.Write(8, str(game.score) + " / " + str(game.scoreThreshold) + " points")
        screen.blit(scoreText, (7*game.config.boardSize[0]*game.config.scaleX/2-scoreText.get_width()/2, game.config.boardTop/2-scoreText.get_height()/2))

        if (game.timeLimit-game.timer)/game.timeLimit-.01 > 0:
            pygame.draw.rect(screen, (255, 0, 0), (0, 98*game.config.scaleY, 100*game.config.scaleX*((game.timeLimit-game.timer)/game.timeLimit-.01), 2*game.config.scaleY))
        # if game.phase == "winning" or game.phase == "starting":
        #     pygame.draw.rect(screen, (0, 255, 0), (0, (10*waitFrame-200)*game.config.scaleY, game.config.scaleX*100*(game.score/game.scoreThreshold), 200*game.config.scaleY))
        # else:
        if game.score > 0:
            pygame.draw.rect(screen, (0, 255, 0), (0, 0, game.config.scaleX*100*(game.score/game.scoreThreshold), 2*game.config.scaleY))
        



    display.blit(screen, (0, 0)) 
    pygame.display.update()
