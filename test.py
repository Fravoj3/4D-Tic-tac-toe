from ursina import *
from matrix import *
from OrbitControls import OrbitControls
from Points import Points

# create a window
grid_size = 3
sphereRadius = 0.05
distanceBetweenSpheres = 4

app = Ursina(title='4D piskvorky', borderless=False)
app.set_background_color((1, 1, 1))

points = Points(size=grid_size, distanceBetweenSpheres=distanceBetweenSpheres, sphereRadius=sphereRadius)


orbitControls = OrbitControls()

def update():
    toatalRotationMatrix = orbitControls.getOrbitMatrix()

    # Transform all points
    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(grid_size):
                for l in range(grid_size):
                    point = points.points[i][j][k][l]
                    old_coords = point.PositionMatrix4d
                    new_coords = multiply_matrices(toatalRotationMatrix, old_coords)
                    point.setObjectPositionByMatrix(stereographic_projection(3, new_coords))
    for line in points.lines.values():
        idA = line.pointA
        idB = line.pointB
        vertAPos = points.points[idA[0]][idA[1]][idA[2]][idA[3]].object.position
        vertBPos = points.points[idB[0]][idB[1]][idB[2]][idB[3]].object.position
        line.object.model.vertices = [vertAPos, vertBPos]
        line.object.model.generate()

    

def input(key):
    # Update scroll direction based on input
    if key == 'scroll up':
        orbitControls.scrollDirection = 'up'
    elif key == 'scroll down':
        orbitControls.scrollDirection = 'down'

app.run()
