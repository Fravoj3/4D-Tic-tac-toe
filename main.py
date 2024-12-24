from ursina import *

app = Ursina(title='4D piskvorky', borderless=False)
window.fps_counter.enabled = False
window.cog_button.enabled = False

app.set_background_color((1, 1, 1))

def startGame():
    print('start game')

name = Button(text='4D tic-tac-toe', color=color.red, position=(0,0.38),font="CascadiaMono-Light.ttf", scale=0)
name.text_entity.world_scale = 2
name.text_entity.font = "CascadiaMono-Light.ttf"
name.text_entity.color = color.black

b = Button(text='Play local multiplayer', color=color.clear, scale=(0.4, 0.08), position=(0, 0.1))
b.text_entity.color = color.black
b.text_entity.world_scale = 1.3

c = Button(text='Play against computer', color=color.clear, scale=(0.4, 0.08), position=(0, 0.0))
c.text_entity.color = color.black
c.text_entity.world_scale = 1.3


author = Text(text='© 2024 Franc Vojtěch', color=color.gray, position=(0.6,-0.4), scale=0.9)


left_line = Entity(
    parent=b,
    model='quad',
    color=color.black,
    scale=(0.1,0.06),  # Thin vertical line
    position=(-0.5, 0, -0.1)  # Left edge of the button
)

right_line = Entity(
    parent=b,
    model='quad',
    color=color.black,
    scale=(0.1,0.06),  # Thin vertical line
    position=(0.5, 0, -0.1)  # Right edge of the button
)

left_line_computer = Entity(
    parent=c,
    model='quad',
    color=color.black,
    scale=(0.1,0.06),  # Thin vertical line
    position=(-0.5, 0, -0.1)  # Left edge of the button
)

right_line_computer = Entity(
    parent=c,
    model='quad',
    color=color.black,
    scale=(0.1,0.06),  # Thin vertical line
    position=(0.5, 0, -0.1)  # Right edge of the button
)

right_line.visible = False
left_line.visible = False
right_line_computer.visible = False
left_line_computer.visible = False

# Define hover behavior
def on_hover():
    left_line.visible = True
    right_line.visible = True

def on_unhover():
    left_line.visible = False
    right_line.visible = False

# Assign hover functions to the button
def update():
    if b.hovered:  # Check if the mouse is over the button
        left_line.visible = True
        right_line.visible = True
        b.text_entity.color = color.rgb(54, 54, 54)
    else:
        left_line.visible = False
        right_line.visible = False
        b.text_entity.color = color.black
    if c.hovered:
        left_line_computer.visible = True
        right_line_computer.visible = True
        c.text_entity.color = color.rgb(54, 54, 54)
    else:
        left_line_computer.visible = False
        right_line_computer.visible = False
        c.text_entity.color = color.black



b.on_click = startGame

app.run()

