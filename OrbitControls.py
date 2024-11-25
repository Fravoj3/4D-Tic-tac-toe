from ursina import *
from matrix import *

class  OrbitControls:
    def __init__(self):
        self.currRotationX = 0
        self.currRotationY = 0
        self.currRotationW = 0

        self.rotationSpeed = 6
        self.rotationRange = 5.5
        self.rotationLeftRight = 0
        self.rotationTopDown = 0
        self.rotationProjection = 0
        self.scrollAmount = pi/16

        self.mouseLeftDown = False
        self.startingMousePos = (0,0)
        self.scroll = 0
        self.firstRun = True
        self.mouseX = 0
        self.mouseY = 0
        
        self.scrollDirection = ''
    
    def getOrbitMatrix(self):
        update = True
        if (mouse.left and not self.mouseLeftDown) or self.firstRun:
            self.firstRun = False
            self.mouseLeftDown = True
            self.currRotationX += self.rotationTopDown
            self.currRotationY -= self.rotationLeftRight
            self.rotationLeftRight = 0
            self.rotationTopDown = 0
            self.startingMousePos = (mouse.x, mouse.y)
        elif mouse.left and self.mouseLeftDown:
            pass
        else:
            if self.mouseLeftDown:
                self.mouseLeftDown = False
            update = False

        if update:
            self.mouseX = mouse.x-self.startingMousePos[0]
            self.mouseY = mouse.y-self.startingMousePos[1]
            self.mouseX *= self.rotationRange
            self.mouseY *= self.rotationRange
        self.rotationLeftRight = lerp(self.rotationLeftRight, self.mouseX, time.dt*self.rotationSpeed)
        self.rotationTopDown = lerp(self.rotationTopDown, self.mouseY, time.dt*self.rotationSpeed)
        # scroll
        if self.scrollDirection == 'up':
            self.scroll += self.scrollAmount
            self.scrollDirection = ''
        elif self.scrollDirection == 'down':
            self.scroll -= self.scrollAmount
            self.scrollDirection = ''
        self.rotationProjection = lerp(self.rotationProjection, self.scroll, time.dt*self.rotationSpeed)


        horizontalRotationMatrix = get_rotation_matrix("x", self.currRotationX  + self.rotationTopDown)
        verticalRotationMatrix = get_rotation_matrix("y", self.currRotationY - self.rotationLeftRight)
        projectionMatrix = get_rotation_matrix("w2", self.rotationProjection)
        allRotations = multiply_matrices(multiply_matrices(horizontalRotationMatrix, verticalRotationMatrix), projectionMatrix)

        toatalRotationMatrix = allRotations
        return toatalRotationMatrix
