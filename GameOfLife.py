import sublime
import sublime_plugin

class SimulateCommand(sublime_plugin.TextCommand):

    running = False

    def run(self, edit):

        if running:
            # the game of life is already running - the user wants to revert the game
            # stop game of life, revert to original file contents

        else:
            # back up file contents to revert to later
            # run game of life at interval of x seconds
            # parts which match the \w regex are deemed living, everything else is considered dead

        running = not running

    def living(char):
        return ord('a') <= ord(char.lower()) <= ord('z')

    def generateLivingCharacter(livingCharacters):
        # generates a living character based on the ord value of the letters, along with the capitalization

        avg = int(sum([ord(l.lower()) for l in livingCharacters]) / len(livingCharacters))
        uppercaseProbability = sum([l.upper() == l for l in livingCharacters]) / len(livingCharacters)
        
