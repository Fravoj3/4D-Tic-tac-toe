from ursina import *

# create a window
grid_size = 4
sphereRadius = 0.035

app = Ursina(title='4D piskvorky', borderless=False)
app.set_background_color((1, 1, 1))

spheres = []
for x in range(grid_size):
    for y in range(grid_size):
        for z in range(grid_size):
            for w in range(grid_size):
                sphere = Entity(model='sphere', color=color.orange, position=(x, y, z), scale=(sphereRadius, sphereRadius, sphereRadius))
                sphere.pos4d = [[x],[y], [z], [w]]
                spheres.append(sphere)

for sphere in spheres:
    sphere.pos4d[0][0] -= 1.5
    sphere.pos4d[1][0] -= 1.5
    sphere.pos4d[2][0] -= 1.5
    sphere.pos4d[3][0] -= 1.5

#player = Entity(model='cube', color=color.orange, scale_y=2)
def get_rotation_matrix(axis, rot):
    if axis=="z":
        return [[cos(rot), -sin(rot),  0 , 0 ],
                [sin(rot),  cos(rot),  0 , 0 ],
                [      0 ,        0 ,  1 , 0 ],
                [      0 ,        0 ,  0 , 1 ]]
    if axis=="y":
        return [[ cos(rot),        0 ,  sin(rot),  0 ],
                [       0 ,        1 ,        0 ,  0 ],
                [-sin(rot),        0 ,  cos(rot),  0 ],
                [       0 ,        0 ,        0 ,  1 ]]
    if axis=="x": 
        return [[  1 ,      0  ,       0  ,  0 ],
                [  0 , cos(rot), -sin(rot),  0 ],
                [  0 , sin(rot),  cos(rot),  0 ],
                [  0 ,      0  ,       0  ,  1 ]]
    if axis=="w":
        return [[ 1 , 0 ,      0  ,       0  ],
                [ 0 , 1 ,      0  ,       0  ],
                [ 0 , 0 , cos(rot), -sin(rot)],
                [ 0 , 0 , sin(rot),  cos(rot)]]
    if axis=="w2":
        return [[   1 ,       0 ,        0 ,       0  ],
                [   0 , cos(rot),        0 ,  sin(rot)],
                [   0 ,       0 ,        1 ,        0 ],
                [   0 ,-sin(rot),        0 ,  cos(rot)]]

def get_position_matrix(object):
    return [[object.x],
            [object.y],
            [object.z]]

def set_position_by_matrix(object, matrix):
    object.x = matrix[0][0]
    object.y = matrix[1][0]
    object.z = matrix[2][0]

def multiply_matrices(a, b):
    if len(a[0]) != len(b):
        print("Matrix multiplication error: incompatible dimensions")
        return None

    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            row.append(sum([a[i][k] * b[k][j] for k in range(len(a[0]))]))
        result.append(row)
    return result

def stereographic_projection(lw, coords):
    w = coords[3][0]
    matrix = [[ 1/(lw-w) ,    0    ,    0    ,    0 ],
              [     0    , 1/(lw-w),    0    ,    0 ],
              [     0    ,    0    , 1/(lw-w),    0 ]]
    return multiply_matrices(matrix, coords)

def dot(vec1, vec2):
    return sum([vec1[i][0]*vec2[i][0] for i in range(len(vec1))])

def norm(vec):
    return sqrt(dot(vec, vec))

def getRotation(vec1, vec2):
    return acos(dot(vec1, vec2)/(norm(vec1)*norm(vec2)))

def lerp(start, end, t):
    return start + t * (end - start)



rot = 0
rot2 = 0

currRotationX = 0
currRotationY = 0

rotationSpeed = 6
rotationRange = 5.5
rotationLeftRight = 0
rotationTopDown = 0

mouseLeftDown = False
startingMousePos = (0,0)
firstRun = True
sliding = False
slidingTime = 0.1
mouseX = 0
mouseY = 0
def update():
    global rot, rot2, rotationSpeed, mouseLeftDown, startingMousePos, currRotationX, currRotationY, rotationLeftRight, rotationTopDown, firstRun, mouseX, mouseY


    update = True
    if (mouse.left and not mouseLeftDown) or firstRun:
        firstRun = False
        mouseLeftDown = True
        currRotationX += rotationTopDown
        currRotationY -= rotationLeftRight
        rotationLeftRight = 0
        rotationTopDown = 0
        startingMousePos = (mouse.x, mouse.y)
    elif mouse.left and mouseLeftDown:
        pass
    else:
        if mouseLeftDown:
            mouseLeftDown = False
        update = False

    if update:
        mouseX = mouse.x-startingMousePos[0]
        mouseY = mouse.y-startingMousePos[1]
        mouseX *= rotationRange
        mouseY *= rotationRange
    rotationLeftRight = lerp(rotationLeftRight, mouseX, time.dt*rotationSpeed)
    rotationTopDown = lerp(rotationTopDown, mouseY, time.dt*rotationSpeed)


    horizontalRotationMatrix = get_rotation_matrix("x", currRotationX  + rotationTopDown)
    verticalRotationMatrix = get_rotation_matrix("y", currRotationY - rotationLeftRight
)
        #rotation_matrix2 = get_rotation_matrix("w2", rot2)
        #new_coords = multiply_matrices(rotation_matrix2, multiply_matrices(rotation_matrix, sphere.pos4d))

    toatalRotationMatrix = multiply_matrices(horizontalRotationMatrix, verticalRotationMatrix)
        #topPointingVectorCopy = multiply_matrices(toatalRotationMatrix, topPointingVector)
        #disalignmentFromZ = getRotation(topPointingVectorCopy, leftPointingVector)
        #compenzateRotationZ = get_rotation_matrix("z", -disalignmentFromZ)
        #topPointingVectorCopy = multiply_matrices(compenzateRotationZ, topPointingVectorCopy)
        #disalignmentFromX = getRotation(topPointingVectorCopy, zPointingVector)
        #compenzateRotationX = get_rotation_matrix("x", -disalignmentFromX)
        #compenzateRotationMatrix = multiply_matrices(compenzateRotationX, compenzateRotationZ)

        #toatalRotationMatrix = multiply_matrices(compenzateRotationMatrix, toatalRotationMatrix)



    for sphere in spheres:
        new_coords = multiply_matrices(toatalRotationMatrix, sphere.pos4d)

        #sphere.pos4d = new_coords
        set_position_by_matrix(sphere, stereographic_projection(3.3, new_coords))


app.run()
