from Basics import *


class Stack():
    def __init__(self, game : Game, color : str, boxes : list):
        self.game = game
        self.type = color
        self.artifacts = []
        self.stack = []
        self.backup = boxes
        self.setup()


    def setup(self):
        self.stack = []
        for b in self.backup:
            self.stack.append(Box(self, b))
        print (self.artifacts)
        if self.artifacts != []:
            for a in self.artifacts:
                a.apply(self)
                print(a.name)
        for b in self.stack:
            b.setup()
        self.pool = []

    

    def trigger(self, matches : list):
        longestMatch = 0
        for m in matches:
            if m[0] == self.type and m[4] > longestMatch:
                longestMatch = m[4]
        if longestMatch > 0 and self.pool == []:
            self.pool.append(self.stack.pop(0))
        empties = []
        for b in range(len(self.pool)):
            if self.pool[b].trigger(longestMatch):
                empties.append(b)
        for b in reversed(range(len(empties))):
            self.pool.pop(empties[b])




class Box():
    def __init__(self, stack : Stack, attributes : list):
        self.stack = stack
        self.basePower = attributes[0]
        self.power = self.basePower
        self.fourMatch = attributes[1]
        self.fiveMatch = attributes[2]
        if len(attributes) >= 3:
            self.bonuses = attributes[3:]
        else:
            self.bonuses = [""]
        self.timer = 0
        self.retriggered = 0
        


    def setup(self):
        self.power = self.basePower
        self.render()

    def render(self):
        self.image = self.stack.game.config.Write(3, str(self.power) + "  " + str(self.fourMatch) + "  " + str(self.fiveMatch) + " " + "; ".join(self.bonuses), 5)

    

    def trigger(self, matchLength : int):
        if matchLength == 0:
            if "mandatory" in self.bonuses:
                self.stack.stack.insert(0, self.reset())
            else:
                self.stack.stack.append(self.reset())
            return True
        else:
            if matchLength == 4:
                self.power += self.fourMatch
                self.render()
            elif matchLength == 5:
                self.power += self.fiveMatch
                self.render()
            self.timer += 1
            if ("fast" in self.bonuses and self.timer >= 1) or (self.timer >= 2) or ("slow" in self.bonuses and self.timer >= 3):
                if "points" in self.bonuses:
                    print(self.power)
                    self.stack.game.score += self.power
                if "timer" in self.bonuses:
                    self.stack.game.timer -= self.power*200
                if "regenerate" in self.bonuses and self.power > 0:
                    self.stack.game.board.fill()
                self.stack.stack.append(self)
                if "retrigger" in self.bonuses:
                    if self.retriggered:
                        self.retriggered = 0
                        return True
                    else:
                        self.retriggered = 1
                        return False
                elif "cumulative" in self.bonuses:
                    self.stack.pool.append(self.stack.stack.pop(0))
                    self.stack.pool[len(self.stack.pool)-1].trigger(matchLength)
                    return False
                elif not "endless" in self.bonuses:
                    return True
            return False
    

    def reset(self):
        self.timer = 0
        if not "growth" in self.bonuses:
            self.power = self.basePower
        self.render()
        return self
    


class Artifact():
    def __init__(self, game : Game, name : str):
        self.game = game
        self.name = name
    


    def apply(self, stack : Stack):
        print(stack)
        if self.name == "Middle Out":
            if len(stack.stack) > 1:
                print("worked?")
                stack.stack.pop(1)
        elif self.name == "End Shuffle":
            if len(stack.stack) > 0:
                stack.stack[len(stack.stack)-1] = Box(stack, [1, 0, 0, "regenerate"])
        elif self.name == "Ignore 4/5 Matches":
            if len(stack.stack) > 0:
                for b in stack.stack:
                    b.basePower += b.fourMatch + floor(b.fiveMatch*0.5)
                    b.fourMatch = 0
                    b.fiveMatch = 0
        elif self.name == "First Time":
            if len(stack.stack) > 0:
                stack.stack[0].bonuses.append("timer")
        elif self.name == "4/5 Match +3/6":
            if len(stack.stack) > 0:
                for b in stack.stack:
                    b.fourMatch += 3
                    b.fiveMatch += 6
        elif self.name == "Aggregate":
            if len(stack.stack) > 0:
                temp = [-1, 0, 0, 0, []]
                for b in stack.stack:
                    temp[0] += 1
                    temp[1] += b.basePower 
                    temp[2] += b.fourMatch
                    temp[3] += b.fiveMatch
                    for a in b.bonuses:
                        temp[4].append(a)
                temp[4] = set(temp[4])
                stack.stack = []
                if temp[0] > 0:
                    for c in range(temp[0]):
                        stack.append(Box(stack, [0, 0, 0]))
                for a in temp[4]:
                    temp.append(a)
                temp.pop(0)
                temp.pop(3)
                stack.append(Box(stack, temp))