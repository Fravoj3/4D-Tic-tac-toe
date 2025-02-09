from ursina import *

class Graph:

    class Line:
        def __init__(self, A, B, points, distanceBetweenSpheres):
            self.pointA = A
            self.pointB = B
            self.points = points
            vec1 = Vec3((A[0]-1)*distanceBetweenSpheres, (A[1]-1)*distanceBetweenSpheres, (A[2]-1)*distanceBetweenSpheres)
            vec2 = Vec3((B[0]-1)*distanceBetweenSpheres, (B[1]-1)*distanceBetweenSpheres, (B[2]-1)*distanceBetweenSpheres)
            self.object = Entity(model=Mesh(
            vertices=[vec1, vec2],  # The two endpoints of the line
            mode='line',  # Render the mesh as a line¨
            thickness=0.006,  # The thickness of the line
            ),color=color.rgb(208, 208, 208))
            #self.object = Entity(model=Pipe(path=(vec1, vec2), cap_ends=False, thicknesses=((0.01, 0.01))), color=color.gray)

    class Point:
        def __init__(self, position: tuple, sphereRadius: int):
            self.sphereRadius = sphereRadius
            self.object = Entity(model='sphere', color=color.orange, position=(position[0], position[1], position[2]), scale=(sphereRadius, sphereRadius, sphereRadius), collider="sphere")
            self.PositionMatrix4d = [[position[0]], [position[1]], [position[2]], [position[3]]]

        def setObjectPositionByMatrix(self, matrix):
            self.object.x = matrix[0][0]
            self.object.y = matrix[1][0]
            self.object.z = matrix[2][0]

    def __init__(self, size, distanceBetweenSpheres, sphereRadius, vertexClickFunction):
        self.sphereRadius = sphereRadius
        self.distanceBetweenSpheres= distanceBetweenSpheres
        self.points = []
        self.lines = []
        # Vytvoření vrcholů a přidání nediagonálních hran
        for i in range(size):
            self.points.append([])
            for j in range(size):
                self.points[i].append([])
                for k in range(size):
                    self.points[i][j].append([])
                    for l in range(size):
                        position = ((i-1)*distanceBetweenSpheres, (j-1)*distanceBetweenSpheres, (k-1)*distanceBetweenSpheres, (l-1)*distanceBetweenSpheres)
                        self.points[i][j][k].append(Graph.Point(position, sphereRadius))
                        isI = i < size - 1
                        isJ = j < size - 1
                        isK = k < size - 1
                        isL = l < size - 1
                        # Nediagonální směry
                        if isI:
                            self.lines.append(Graph.Line((i, j, k, l), (i+1, j, k, l),self.points, distanceBetweenSpheres))
                        if isJ:
                            self.lines.append(Graph.Line((i, j, k, l), (i, j+1, k, l),self.points, distanceBetweenSpheres))
                        if isK:
                            self.lines.append(Graph.Line((i, j, k, l), (i, j, k+1, l),self.points, distanceBetweenSpheres))
                        if isL:
                            self.lines.append(Graph.Line((i, j, k, l), (i, j, k, l+1),self.points, distanceBetweenSpheres))
        
        # Přidání diagonálních směrů  
        added_set = set()
        startingPointSet = set()

        def addLines(vector, startingPoint):
            if (vector[0]*-1, vector[1]*-1, vector[2]*-1, vector[3]*-1) in added_set:
                return
            added_set.add(tuple(vector))
            newPoint = startingPoint
            for i in range(1, size):
                oldPoint = tuple(newPoint)
                newPoint = [newPoint[0] + vector[0], newPoint[1] + vector[1], newPoint[2] + vector[2], newPoint[3] + vector[3]]
                self.lines.append(Graph.Line(oldPoint, tuple(newPoint), self.points, distanceBetweenSpheres))

        def permutate(vec, function, val: list = []):
            if len(val) == 4:
                function(val)
                return
            else:
                set_vec = set(vec)
                for i in set_vec:
                    copyedVec = vec.copy()
                    copyedVec.remove(i)
                    permutate(copyedVec, function, val+[i])
        
        def getComponentValue(value):
            if value == 1:
                return 0
            if value == -1:
                return size-1
            if value == 0:
                return 0
            
        def addDiagonalLines(vector):
            if tuple(vector) in added_set:
                return
            if (vector[0]*-1, vector[1]*-1, vector[2]*-1, vector[3]*-1) in added_set:
                return
            added_set.add(tuple(vector))
            startingPoint = (getComponentValue(vector[0]), getComponentValue(vector[1]), getComponentValue(vector[2]), getComponentValue(vector[3]))
            addLines(vector, startingPoint)

        def getStartingPoints(vector, point, function, orgVecotr):
            if len(vector) == 0:
                if tuple(point) in startingPointSet:
                    return
                startingPointSet.add(tuple(point))
                function(orgVecotr, point)
                return
            if vector[0] == 0:
                point2 = point.copy()
                point2.append(0)
                getStartingPoints(vector[1:], point2, function, orgVecotr)
                point2 = point.copy()
                point2.append(1)
                getStartingPoints(vector[1:], point2, function, orgVecotr)
                point2 = point.copy()
                point2.append(2)
                getStartingPoints(vector[1:], point2, function, orgVecotr)
            else:
                point2 = point.copy()
                point2.append(getComponentValue(vector[0]))
                getStartingPoints(vector[1:], point2, function, orgVecotr)

        def addSecondaryDiagonalLines(vector):
            startingPointSet.clear()
            getStartingPoints(vector, [], addLines, vector)

        # Hlavní diagonály tělesa
        permutate([1, 1, 1, -1], addDiagonalLines, [])
        permutate([1, 1, -1, -1], addDiagonalLines, [])
        addLines([1, 1, 1, 1], (0, 0, 0, 0))

        # Doplňkové diagonály tělesa
        #
        # permutate([1, 1, 1, 0], addSecondaryDiagonalLines, [])
        #permutate([1, 1, -1, 0], addSecondaryDiagonalLines, [])
        #permutate([1, 1, 0, 0], addSecondaryDiagonalLines, [])
        #permutate([1, -1, 0, 0], addSecondaryDiagonalLines, [])
        #permutate([1, 0, 0, 0], addSecondaryDiagonalLines, [])

    def hide(self):
        for point in self.points:
            for point2 in point:
                for point3 in point2:
                    for point4 in point3:
                        point4.object.visible = False
        for line in self.lines:
            line.object.visible = False

    def show(self):
        for point in self.points:
            for point2 in point:
                for point3 in point2:
                    for point4 in point3:
                        point4.object.visible = True
        for line in self.lines:
            line.object.visible = True        
                       
    def restartColors(self):
        for point in self.points:
            for point2 in point:
                for point3 in point2:
                    for point4 in point3:
                        point4.object.color = color.orange
        for line in self.lines:
            line.object.color = color.rgb(208, 208, 208)	

    def colorizePoint(self, i, j, k, l, color):
        self.points[i][j][k][l].object.color = color
        for line in self.lines:
            if (line.pointA == (i, j, k, l) or line.pointB == (i, j, k, l)) and \
            (self.points[line.pointA[0]][line.pointA[1]][line.pointA[2]][line.pointA[3]].object.color == color and \
             self.points[line.pointB[0]][line.pointB[1]][line.pointB[2]][line.pointB[3]].object.color == color):
                line.object.color = color
