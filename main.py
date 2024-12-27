from ursina import *
import mainScreen
import game

'''
    4D tic-tac-toe
    author: Franc Vojtěch
    date: 27. 12. 2024
'''

# Display window with the game
app = Ursina(title='4D piskvorky', borderless=False)
window.fps_counter.enabled = False
window.cog_button.enabled = False
app.set_background_color((1, 1, 1))

# Display the main screen
def startMultiGame():
    gameInstance.show()
    mainScreenInstance.hideScreen()
    gameInstance.restartGame()
    gameInstance.startGame(True, True)

def startSingleGame():
    gameInstance.show()
    mainScreenInstance.hideScreen()
    gameInstance.restartGame()
    gameInstance.startGame(False, True)	

def returnToMenu():
    gameInstance.hide()
    mainScreenInstance.showScreen()

mainScreenInstance = mainScreen.MainScreen(startMultiGame, startSingleGame)
mainScreenInstance.showScreen()

gameInstance = game.Game(0.09, 4, returnToMenu)
gameInstance.hide()


def update():
    mainScreenInstance.update()
    gameInstance.update()

def input(key):
    gameInstance.input(key)

app.run()

