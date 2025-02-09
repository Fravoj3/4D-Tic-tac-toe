from ursina import *

class MainScreen:
    '''
    Class responsible for the main screen of the game, constructor takes two functions as arguments, which are called when the buttons are clicked.
    '''
    def __init__(self, newMultiplayerFc, newSingleplayerFc):
        self.newMultiplayerFc = newMultiplayerFc
        self.newSingleplayerFc = newSingleplayerFc
        self.createScreen()
        self.visible = True

    def createScreen(self):
        self.title = Button(text='4D tic-tac-toe', color=color.red, position=(0,0.38),font="CascadiaMono-Light.ttf", scale=0)
        self.title.text_entity.world_scale = 2
        self.title.text_entity.font = "CascadiaMono-Light.ttf"
        self.title.text_entity.color = color.black

        self.playMultiplayerButton = Button(text='Play local multiplayer', color=color.clear, scale=(0.4, 0.08), position=(0, 0.1))
        self.playMultiplayerButton.text_entity.color = color.black
        self.playMultiplayerButton.text_entity.world_scale = 1.3

        self.playSingleplayerButton = Button(text='Play against computer', color=color.clear, scale=(0.4, 0.08), position=(0, 0.0))
        self.playSingleplayerButton.text_entity.color = color.black
        self.playSingleplayerButton.text_entity.world_scale = 1.3


        self.authorText = Text(text='© 2024 Franc Vojtěch', color=color.gray, position=(0.6,-0.4), scale=0.9)

        self.multiButtonLLine = Entity(
            parent=self.playMultiplayerButton,
            model='quad',
            color=color.black,
            scale=(0.1,0.06),  # Thin vertical line
            position=(-0.5, 0, -0.1)  # Left edge of the button
        )

        self.multiButtonRLine = Entity(
            parent=self.playMultiplayerButton,
            model='quad',
            color=color.black,
            scale=(0.1,0.06),  # Thin vertical line
            position=(0.5, 0, -0.1)  # Right edge of the button
        )

        self.singleButtonLLine = Entity(
            parent=self.playSingleplayerButton,
            model='quad',
            color=color.black,
            scale=(0.1,0.06),  # Thin vertical line
            position=(-0.5, 0, -0.1)  # Left edge of the button
        )

        self.singleButtonRLine = Entity(
            parent=self.playSingleplayerButton,
            model='quad',
            color=color.black,
            scale=(0.1,0.06),  # Thin vertical line
            position=(0.5, 0, -0.1)  # Right edge of the button
        )

        self.multiButtonLLine.visible = False
        self.multiButtonRLine.visible = False
        self.singleButtonLLine.visible = False
        self.singleButtonRLine.visible = False

        self.playMultiplayerButton.on_click = self.newMultiplayerFc
        self.playSingleplayerButton.on_click = self.newSingleplayerFc

    def hideScreen(self):
        self.title.visible = False
        self.playMultiplayerButton.visible = False
        self.playSingleplayerButton.visible = False
        self.authorText.visible = False
        self.multiButtonLLine.visible = False
        self.multiButtonRLine.visible = False
        self.singleButtonLLine.visible = False
        self.singleButtonRLine.visible = False
        self.visible = False

        self.title.disable()
        self.playMultiplayerButton.disable()
        self.playSingleplayerButton.disable()
        self.authorText.disable()
        self.multiButtonLLine.disable()
        self.multiButtonRLine.disable()
        self.singleButtonLLine.disable()
        self.singleButtonRLine.disable()
        self.visible = False

    def showScreen(self):
        self.title.visible = True
        self.playMultiplayerButton.visible = True
        self.playSingleplayerButton.visible = True
        self.authorText.visible = True
        self.multiButtonLLine.visible = False
        self.multiButtonRLine.visible = False
        self.singleButtonLLine.visible = False
        self.singleButtonRLine.visible = False
        self.visible = True

        self.title.enable()
        self.playMultiplayerButton.enable()
        self.playSingleplayerButton.enable()
        self.authorText.enable()
        self.multiButtonLLine.enable()
        self.multiButtonRLine.enable()
        self.singleButtonLLine.enable()
        self.singleButtonRLine.enable()
        self.visible = True

    def update(self):
        if not self.visible:
            return
        
        if self.playMultiplayerButton.hovered:  # Check if the mouse is over the button
            self.multiButtonLLine.visible = True
            self.multiButtonRLine.visible = True
            self.playMultiplayerButton.text_entity.color = color.rgb(54, 54, 54)
        else:
            self.multiButtonLLine.visible = False
            self.multiButtonRLine.visible = False
            self.playMultiplayerButton.text_entity.color = color.black
        if self.playSingleplayerButton.hovered:
            self.singleButtonLLine.visible = True
            self.singleButtonRLine.visible = True
            self.playSingleplayerButton.text_entity.color = color.rgb(54, 54, 54)
        else:
            self.singleButtonLLine.visible = False
            self.singleButtonRLine.visible = False
            self.playSingleplayerButton.text_entity.color = color.black
