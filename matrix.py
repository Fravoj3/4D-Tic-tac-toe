from math import *

def get_rotation_matrix(axis, rot):
    '''
    Returns the 4x4 rotation matrix for a given axis and rotation angle.

    :param axis: the axis to rotate around, can be "x", "y", "z", "w" or "w2"
    :param rot: the rotation angle in radians
    :return: the 4x4 rotation matrix
    '''
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
    '''
    Returns the position of an ursina object as a 3x1 matrix.

    :param object: the ursina object to get the position from
    :return: the 3x1 matrix containing the position of the object
    '''
    return [[object.x],
            [object.y],
            [object.z]]

def set_position_by_matrix(object, matrix):
    '''
    sets the position of an ursina object to the given matrix.

    :param object: the ursina object to be moved
    :param matrix: the at least 3x1 matrix containing the new position
    '''
    object.x = matrix[0][0]
    object.y = matrix[1][0]
    object.z = matrix[2][0]

def multiply_matrices(a, b):
    '''
    multiplies two given matrices, in case of incompatible dimensions, it prints an error message and returns None.

    :param a: the first matrix at the left side of the multiplication
    :param b: the second matrix at the right side of the multiplication
    :return: the resulting matrix of the multiplication
    '''
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

def norm(vec):
    # Returns normalized vector
    return [vec[i][0]/sqrt(sum([vec[j][0]**2 for j in range(len(vec))])) for i in range(len(vec))]

def stereographic_projection(lw, coords):
    ''' 
    creates the stereographic projection of a 4D point onto a 3D space.

    :param lw: the distance of light source in the 4th dimension
    :param coords: the 4D coordinates of the point
    :return: the 3D coordinates vector of the point    
    '''
    w = coords[3][0]
    dist = (lw-(w/3.5))
    matrix = [[ 1/dist ,    0    ,    0    ,    0 ],
              [     0    , 1/dist,    0    ,    0 ],
              [     0    ,    0    , 1/dist,    0 ]]
    return multiply_matrices(matrix, coords)

def dot(vec1, vec2):
    # Returns the dot product of two vectors
    return sum([vec1[i][0]*vec2[i][0] for i in range(len(vec1))])

def getRotation(vec1, vec2):
    # Returns the angle between two vectors in radians
    return acos(dot(vec1, vec2)/(norm(vec1)*norm(vec2)))
