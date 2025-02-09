import threading
from ursina import *
from matrix import *
from OrbitController import OrbitController
from Graph import Graph
from gameRepresentation import GameRepresentation

class Game:
    def __init__(self, sphereRadius, distanceBetweenSpheres, returnToMenuFc):
        self.grid_size = 3
        self.sphereRadius = sphereRadius
        self.distanceBetweenSpheres = distanceBetweenSpheres
        self.returnToMenuFc = returnToMenuFc

        self.graph = Graph(size=self.grid_size, distanceBetweenSpheres=self.distanceBetweenSpheres, sphereRadius=self.sphereRadius, vertexClickFunction=self.onClickOnVertex)
        self.orbitController = OrbitController()
        self.visible = True
        self.waitingForAIMove = False

        self.color1 = color.green
        self.color2 = color.blue

        self.currPlayerTextLabel = Text(text="Current player", position=(-0.86, 0.46), scale=0.8, color=color.black)
        self.currPlayerText = Text(text="Green player", position=(-0.86, 0.43), scale=1.6, color=color.black)
        self.playAgainButton = Button(text='Play again', scale=(0.28, 0.04), position=(-0.725, 0.36), color=color.black, visible=False, enabled=False)
        self.returnToMenuButton = Button(text='Return to menu', scale=(0.28, 0.04), position=(-0.725, 0.31), color=color.black, visible=False, enabled=False)

    def update(self):
        toatalRotationMatrix = self.orbitController.getOrbitMatrix()

        # Transform all points
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                for k in range(self.grid_size):
                    for l in range(self.grid_size):
                        point = self.graph.points[i][j][k][l]
                        old_coords = point.PositionMatrix4d
                        new_coords = multiply_matrices(toatalRotationMatrix, old_coords)
                        point.setObjectPositionByMatrix(stereographic_projection(3, new_coords))
        for line in self.graph.lines:
            idA = line.pointA
            idB = line.pointB
            vertAPos = self.graph.points[idA[0]][idA[1]][idA[2]][idA[3]].object.position
            vertBPos = self.graph.points[idB[0]][idB[1]][idB[2]][idB[3]].object.position
            line.object.model.vertices = [vertAPos, vertBPos]
            line.object.model.generate()

    def hide(self):
        self.visible = False
        self.graph.hide()
        self.currPlayerTextLabel.enabled = False
        self.currPlayerText.enabled = False
        self.currPlayerTextLabel.visible = False
        self.currPlayerText.visible = False
        self.playAgainButton.enabled = False
        self.returnToMenuButton.visible = False
        self.returnToMenuButton.enabled = False

    def show(self):
        self.visible = True
        self.graph.show()
        self.currPlayerTextLabel.enabled = True
        self.currPlayerText.enabled = True
        self.currPlayerTextLabel.visible = True
        self.currPlayerText.visible = True
        self.playAgainButton.visible = False
        self.playAgainButton.enabled = False
        self.returnToMenuButton.visible = False
        self.returnToMenuButton.enabled = False

    def input(self, key):
        # Update scroll direction based on input
        if key == 'scroll up':
            self.orbitController.scrollDirection = 'up'
        elif key == 'scroll down':
            self.orbitController.scrollDirection = 'down'
        
        if key == 'left mouse up':
            if mouse.hovered_entity:  # Check if a 3D object was under the mouse when released
                for i in range(self.grid_size):
                    for j in range(self.grid_size):
                        for k in range(self.grid_size):
                            for l in range(self.grid_size):
                                if mouse.hovered_entity == self.graph.points[i][j][k][l].object:
                                    self.onClickOnVertex(i, j, k, l)

    def restartGame(self):
        self.graph.restartColors()
        self.multiplayer = False
        self.humanStarts = False
        self.gameOver = False
        self.waitingForAIMove = False
        self.currentPlayer = 1
        self.gameRepresentation = GameRepresentation(1)
        self.gameRepresentation.createNewGame()

    def startGame(self, multiplayer, starts1):
        self.multiplayer = multiplayer
        self.gameOver = False
        self.currentPlayer = 1 if starts1 else 2
        self.currPlayerTextLabel.text = "Current player"
        if multiplayer:
            self.currPlayerText.text = "Green player"
        else:
            self.currPlayerText.text = "You"

    def onClickOnVertex(self, i, j, k, l):
        if self.gameOver:
            return
        
        if self.multiplayer:
            self.makeMultiplayerMove(i, j, k, l)
        else:
            self.makeSingleplayerMove(i, j, k, l)
        
    def makeSingleplayerMove(self, i, j, k, l):
        if self.waitingForAIMove:
            return
        self.waitingForAIMove = True
        # check if move is valid
        if self.gameRepresentation.gameMove.board[i][j][k][l].player != 0:
            self.waitingForAIMove = False
            return
        # colorize the point
        self.graph.colorizePoint(i, j, k, l, self.color1)
        self.gameRepresentation.makeMove((i, j, k, l))
        # Evaluete game move and detect if game is over
        eval = self.gameRepresentation.gameMove.evaluate()
        if eval == -1:
            self.gameOver = True
            self.currPlayerTextLabel.text = "Game over"
            self.currPlayerText.text = "You won"
            self.waitingForAIMove = False
            self.showPlayAgainButton()
            return
        elif eval == 0:
            self.gameOver = True
            self.currPlayerTextLabel.text = "Game over"
            self.currPlayerText.text = "Draw"
            self.waitingForAIMove = False
            self.showPlayAgainButton()
            return

        # Computer's turn
        def makeCopmutersTurn(self):
            a, b, c, d = self.gameRepresentation.getAndMakeBestMove(3)
            self.graph.colorizePoint(a, b, c, d, self.color2)
            eval = self.gameRepresentation.gameMove.evaluate()
            if eval == 1:
                self.gameOver = True
                self.currPlayerTextLabel.text = "Game over"
                self.currPlayerText.text = "Computer won"
                self.showPlayAgainButton()
                return
            elif eval == 0:
                self.gameOver = True
                self.currPlayerTextLabel.text = "Game over"
                self.currPlayerText.text = "Draw"
                self.showPlayAgainButton()
                return
            self.currPlayerText.text = "You"
            self.waitingForAIMove = False

        
        self.currPlayerText.text = "Computer's turn"
        p1 = threading.Thread(target=makeCopmutersTurn, args=(self,))
        p1.start()

    def makeMultiplayerMove(self, i, j, k, l):
        # check if move is valid
        if self.gameRepresentation.gameMove.board[i][j][k][l].player != 0:
            return
        # colorize the point
        if self.currentPlayer == 1:
            self.graph.colorizePoint(i, j, k, l, self.color1)
            self.gameRepresentation.gameMove.board[i][j][k][l].player = 1
            self.currentPlayer = 2
            self.currPlayerText.text = "Blue player"
        else:
            self.graph.colorizePoint(i, j, k, l, self.color2)
            self.gameRepresentation.gameMove.board[i][j][k][l].player = 2
            self.currentPlayer = 1
            self.currPlayerText.text = "Green player"

        self.gameRepresentation.makeMove((i, j, k, l))
        # Evaluete game move and detect if game is over
        eval = self.gameRepresentation.gameMove.evaluate()
        if eval is not None:
            self.currPlayerTextLabel.text = "Game over"
            self.gameOver = True
            self.showPlayAgainButton()
        if eval == -1:
            self.currPlayerText.text = "Green player wins"
        elif eval == 1:
            self.currPlayerText.text = "Blue player wins"
        elif eval == 0:
            self.currPlayerText.text = "Draw"

    def showPlayAgainButton(self):
        self.playAgainButton.visible = True
        self.playAgainButton.enabled = True
        self.returnToMenuButton.visible = True
        self.returnToMenuButton.enabled = True
        self.returnToMenuButton.on_click = self.returnToMenuFc
        def restartGame():
            mp = self.multiplayer
            self.restartGame()
            self.startGame(mp, True)
            self.playAgainButton.visible = False
            self.playAgainButton.enabled = False
            self.returnToMenuButton.visible = False
            self.returnToMenuButton.enabled = False
        self.playAgainButton.on_click = restartGame
