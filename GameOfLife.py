import sublime
import sublime_plugin
import random
import copy


class AnimateCommand(sublime_plugin.TextCommand):
    lastGrid = None

    def run(self, edit, firstTime):
        # if not running:
        #     return

        tabSize = self.view.settings().get("tab_size")

        # print(running)
        # applies animation
        totalRegion = sublime.Region(0, self.view.size())
        if firstTime or not self.lastGrid:
            self.lastGrid = []
            lines = self.view.lines(totalRegion)
            for r in range(len(lines)):
                line = lines[r]

                self.lastGrid.append([])

                for c in range(line.begin(), line.end()):
                    char = sublime.Region(c, c + 1)
                    c = c - line.begin()
                    # we don't want tabs, but rather spaces
                    if self.view.substr(char) == "\t":
                        self.lastGrid[r] += [" "] * tabSize
                    else:
                        self.lastGrid[r].append(self.view.substr(char))

        self.nextFrame(self.lastGrid)

        newContents = ""

        for r in range(len(self.lastGrid)):
            for c in range(len(self.lastGrid[r])):
                newContents += self.lastGrid[r][c]
            newContents += "\n"

        # to get rid of trailing newline
        newContents = newContents[:len(newContents) - 1]

        self.view.replace(edit, totalRegion, newContents)

        # self.lastGrid = grid

        # print(self.lastGrid)

    def getNeighbors(self, grid, row, col):

        neighbors = []

        for r in range(-1, 1 + 1):
            for c in range(-1, 1 + 1):

                if r == c == 0:
                    continue

                nr = row + r
                nc = col + c

                # if this position is defined
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]):

                    cell = grid[nr][nc]
                    if living(cell):

                        neighbors.append(cell)

        return neighbors

    def nextFrame(self, grid):

        # changes which we implement afterwards, to save us from having to
        # deepcopy
        changes = {}

        for r in range(len(grid)):
            for c in range(len(grid[r])):
                cell = grid[r][c]
                neighbors = self.getNeighbors(grid, r, c)

                if living(cell):
                    if 2 <= len(neighbors) <= 3:
                        # cell survives
                        continue
                    else:
                        changes[(r, c)] = " "
                else:
                    if len(neighbors) == 3:
                        changes[(r, c)] = generateLivingCharacter(neighbors)
                    else:
                        changes[(r, c)] = " "

        for coord in changes:
            r = coord[0]
            c = coord[1]
            grid[r][c] = changes[coord]

        return grid


class SimulateCommand(sublime_plugin.TextCommand):

    running = False
    fileBuffer = ""
    edit = None

    def run(self, edit):

        # print("Before", self.running)
        self.edit = edit
        if self.running:
            self.running = False
            self.stopSimulation(edit)
            # the game of life is already running - the user wants to revert the game
            # stop game of life, revert to original file contents

        else:
            self.running = True
            self.startSimulation(edit)
            # back up file contents to revert to later
            # run game of life at interval of x seconds
            # parts which match the \w regex are deemed living, everything else
            # is considered dead

        # print("After", self.running)

    def startSimulation(self, edit):
        fileRegion = sublime.Region(0, self.view.size())

        self.fileBuffer = self.view.substr(fileRegion)

        self.animate(0)

    def stopSimulation(self, edit):
        self.view.replace(
            edit, sublime.Region(0, self.view.size()), self.fileBuffer)

    def animate(self, x):
        if not self.running:
            self.running = False
            return

        firstTime = x == 0

        self.view.run_command("animate", {"firstTime": firstTime})

        if self.running:
            sublime.set_timeout(lambda: self.animate(1), 100)


def living(char):
    return ord('a') <= ord(char.lower()) <= ord('z')


def generateLivingCharacter(livingCharacters):
    # generates a living character based on the ord value of the letters,
    # along with the capitalization

    avg = int(sum([ord(l.lower()) for l in livingCharacters]) /
              len(livingCharacters))  # letter's char code

    char = chr(avg)

    uppercaseProbability = sum(
        [l.upper() == l for l in livingCharacters]) / len(livingCharacters)

    if random.random() < uppercaseProbability:
        char = char.upper()

    return char
