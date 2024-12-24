class Point:
        def __init__(self, player=None):
            if player is None:
                self.player = 0
            else:
                self.player = player
            self.neighboursOnX = 0
            self.neighboursOnY = 0
            self.neighboursOnZ = 0
            self.neighboursOnW = 0

        def copy(self):
            newPoint = Point(self.player)
            newPoint.neighboursOnX = self.neighboursOnX
            newPoint.neighboursOnY = self.neighboursOnY
            newPoint.neighboursOnZ = self.neighboursOnZ
            newPoint.neighboursOnW = self.neighboursOnW
            return newPoint
        
class Move:
    def __init__(self, board, player):
        self.board = board
        self.player = player # 1 or 2
        self.evaluation = None
        self.children = dict()
    
    def evaluate(self):
        '''
        Evaluates board state. Returns player who has won or -1 if no one has won.
        '''
        won = [None, False, False]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        if self.board[i][j][k][l].neighboursOnX >= 3:
                            won[self.board[i][j][k][l].player] = True
                        if self.board[i][j][k][l].neighboursOnY >= 3:
                            won[self.board[i][j][k][l].player] = True
                        if self.board[i][j][k][l].neighboursOnZ >= 3:
                            won[self.board[i][j][k][l].player] = True
                        if self.board[i][j][k][l].neighboursOnW >= 3:
                            won[self.board[i][j][k][l].player] = True
                    
        def diagonalCheck(start, shift):
            for i in range(3):
                if self.board[start[0]+i*shift[0]][start[1]+i*shift[1]][start[2]+i*shift[2]][start[3]+i*shift[3]].player != self.board[start[0]][start[1]][start[2]][start[3]].player:
                    return False
                
            won[self.board[start[0]][start[1]][start[2]][start[3]].player] = True
        # Diagonals check
        diagonalCheck([0, 0, 0, 0], [1, 1, 1, 1])
        diagonalCheck([2, 0, 0, 0], [-1, 1, 1, 1])
        diagonalCheck([0, 2, 0, 0], [1, -1, 1, 1])
        diagonalCheck([0, 0, 2, 0], [1, 1, -1, 1])
        diagonalCheck([0, 0, 0, 2], [1, 1, 1, -1])
        diagonalCheck([0, 0, 2, 2], [1, 1, -1, -1])
        diagonalCheck([0, 2, 0, 2], [1, -1, 1, -1])
        diagonalCheck([2, 0, 0, 2], [-1, 1, 1, -1])
        if won[1] and won[2]:
            return 0
        if won[1]:
            return -1
        if won[2]:
            return 1
        
        return None
    
    def setPoint(self, coords, board):
        '''
        Sets point on the board representing player's move. x, y, z, w, are coordinates of player on given board.
        returns True if player has won in axis x, y, z or w (exceot body diagonals).
        '''
        x, y, z, w = coords
        player = self.player
        def getNeighbourVal(x, y, z, w, dir):
            if x < 0 or y < 0 or z < 0 or w < 0:
                return 0
            if x >= 3 or y >= 3 or z >= 3 or w >= 3:
                return 0
            if board[x][y][z][w].player == player:
                if dir == 'x':
                    return board[x][y][z][w].neighboursOnX
                if dir == 'y':
                    return board[x][y][z][w].neighboursOnY
                if dir == 'z':
                    return board[x][y][z][w].neighboursOnZ
                if dir == 'w':
                    return board[x][y][z][w].neighboursOnW
            return 0
        
        def updateNeighbourVal(x, y, z, w, dir, val):
            if x < 0 or y < 0 or z < 0 or w < 0:
                return
            if x >= 3 or y >= 3 or z >= 3 or w >= 3:
                return
            for i in range(2):
                shift = 0
                while True:
                    if dir == 'x':
                        if x+shift >= 3 or x+shift < 0:
                            break
                        if board[x+shift][y][z][w].player != player:
                            break
                        board[x+shift][y][z][w].neighboursOnX = val
                    if dir == 'y':
                        if y+shift >= 3 or y+shift < 0:
                            break
                        if board[x][y+shift][z][w].player != player:
                            break
                        board[x][y+shift][z][w].neighboursOnY = val
                    if dir == 'z':
                        if z+shift >= 3 or z+shift < 0:
                            break
                        if board[x][y][z+shift][w].player != player:
                            break
                        board[x][y][z+shift][w].neighboursOnZ = val
                    if dir == 'w':
                        if w+shift >= 3 or w+shift < 0:
                            break
                        if board[x][y][z][w+shift].player != player:
                            break
                        board[x][y][z][w+shift].neighboursOnW = val
                    
                    if i == 0:
                        shift -= 1
                    else:
                        shift += 1
        board[x][y][z][w].player = player
        # Max. val. dir x
        val = getNeighbourVal(x-1, y, z, w, 'x') + getNeighbourVal(x+1, y, z, w, 'x') + 1
        updateNeighbourVal(x, y, z, w, 'x', val)
        # Max. val. dir y
        val2 = getNeighbourVal(x, y-1, z, w, 'y') + getNeighbourVal(x, y+1, z, w, 'y') + 1
        updateNeighbourVal(x, y, z, w, 'y', val2)
        # Max. val. dir z
        val3 = getNeighbourVal(x, y, z-1, w, 'z') + getNeighbourVal(x, y, z+1, w, 'z') + 1
        updateNeighbourVal(x, y, z, w, 'z', val3)
        # Max. val. dir w
        val4 = getNeighbourVal(x, y, z, w-1, 'w') + getNeighbourVal(x, y, z, w+1, 'w') + 1
        updateNeighbourVal(x, y, z, w, 'w', val4)
        if val >= 3 or val2 >= 3 or val3 >= 3 or val4 >= 3:
            return True
          
    def evaluateStateForDepth(self, board, minPlayer=True):
        # Detecting near wins
        winMin = 0
        winMax = 0

        # for perpendicular to x, y, z, w vectors
        def evaluateRes(p):
            nonlocal winMin, winMax
            if p[0] == 2 and p[1] == 0:
                winMin += 4
                winMax -= 6
            if p[1] == 2 and p[0] == 0:
                winMax += 4
                winMin -= 6
            if p[0] == 1 and p[1] == 0:
                winMin += 1
            if p[1] == 1 and p[0] == 0:
                winMax += 1

        def evaluatePoint(x, y, z, w, p):
            if board[x][y][z][w].player == 1:
                p[0] += 1
            if board[x][y][z][w].player == 2:
                p[1] += 1

        def tryFitVecotrs(indexForOne):
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        p = [0, 0]
                        if indexForOne == 0:
                            evaluatePoint(0, i, j, k, p)
                            evaluatePoint(1, i, j, k, p)
                            evaluatePoint(2, i, j, k, p)
                        if indexForOne == 1:
                            evaluatePoint(i, 0, j, k, p)
                            evaluatePoint(i, 1, j, k, p)
                            evaluatePoint(i, 2, j, k, p)
                        if indexForOne == 2:
                            evaluatePoint(i, j, 0, k, p)
                            evaluatePoint(i, j, 1, k, p)
                            evaluatePoint(i, j, 2, k, p)
                        if indexForOne == 3:
                            evaluatePoint(i, j, k, 0, p)
                            evaluatePoint(i, j, k, 1, p)
                            evaluatePoint(i, j, k, 2, p)
                        
                        evaluateRes(p)

        tryFitVecotrs(0)
        tryFitVecotrs(1)
        tryFitVecotrs(2)
        tryFitVecotrs(3)
        # for diagonals
        def diagonalCheck(start, shift):
            p = [0, 0]
            for i in range(3):
                evaluatePoint(start[0]+i*shift[0],start[1]+i*shift[1],start[2]+i*shift[2],start[3]+i*shift[3], p)
            evaluateRes(p)
            
                
        # Diagonals check
        diagonalCheck([0, 0, 0, 0], [1, 1, 1, 1])
        diagonalCheck([2, 0, 0, 0], [-1, 1, 1, 1])
        diagonalCheck([0, 2, 0, 0], [1, -1, 1, 1])
        diagonalCheck([0, 0, 2, 0], [1, 1, -1, 1])
        diagonalCheck([0, 0, 0, 2], [1, 1, 1, -1])
        diagonalCheck([0, 0, 2, 2], [1, 1, -1, -1])
        diagonalCheck([0, 2, 0, 2], [1, -1, 1, -1])
        diagonalCheck([2, 0, 0, 2], [-1, 1, 1, -1])

        return winMin if minPlayer else winMax

class MinMax:
    def __init__(self, startingPlayer):
        self.startingPlayer = startingPlayer # 1 or 2

    def createEmptyBoard(self):
        return [[[[Point() for i in range(3)] for j in range(3)] for k in range(3)] for l in range(3)]
    
    def copyBoard(self, board):
        return [[[[board[i][j][k][l].copy() for l in range(3)] for k in range(3)] for j in range(3)] for i in range(3)]
    
    def minimax(self, move, alpha, beta, depth=None):
        move.evaluation = None
        eval = move.evaluate()
        bestMove = None
        if eval is not None:
            move.evaluation = eval
            if depth is not None:
                return eval*10
            return eval
        
        if depth is not None and depth == 0:
            return move.evaluateStateForDepth(move.board, True if move.player == 1 else False)
        if depth is not None:
            depth -= 1
    
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        if move.board[i][j][k][l].player == 0:
                            newBoard = self.copyBoard(move.board)
                            move.setPoint((i, j, k, l), newBoard)
                            newMove = Move(newBoard, 1 if move.player == 2 else 2)
                            e =  self.minimax(newMove, alpha, beta, depth)
                            if move.player == 1 and (move.evaluation is None or e < move.evaluation):
                                move.evaluation = e
                                self.bestMove = newMove
                                self.bestMoveCoords = (i, j, k, l)
                            if move.player == 2 and (move.evaluation is None or e > move.evaluation):
                                move.evaluation = e
                                self.bestMove = newMove
                                self.bestMoveCoords = (i, j, k, l)

                            #move.children[(i, j, k, l)] = newMove

                            if move.evaluation is None:
                                continue

                            if move.player == 1:
                                beta = min(beta, move.evaluation)
                            else:
                                alpha = max(alpha, move.evaluation)

                            if beta <= alpha:
                                return move.evaluation
        if move.evaluation is None:
            return 0
        return move.evaluation
    
    def startMinMax(self):
        move = Move(self.createEmptyBoard(), self.startingPlayer)
        self.minimax(move, -1, 1, 3)
        print(move.evaluation)

    def createNewGame(self):
        self.gameStartingMove = Move(self.createEmptyBoard(), self.startingPlayer)
        self.gameMove = self.gameStartingMove
    
    def getAndMakeBestMove(self, depth):
        self.minimax(self.gameMove, -1, 1, depth)
        self.gameMove = self.bestMove
        return self.bestMoveCoords
    
    def makeMove(self, coords):
        self.gameMove.setPoint(coords, self.gameMove.board)

if __name__ == "__main__":
    minmax = MinMax(1)
    minmax.createNewGame()
    player = int(input("Write 1 if you want to start, 2 if you want to be second: "))
    while True:
        if player == 1:
            print("Write coordinates for your move: ")
            coords = [int(i) for i in input().split()]
            minmax.makeMove(coords)
            player = 2
        else:
            coords = minmax.getAndMakeBestMove(3)
            print("Computer moved to: ", coords)
            player = 1
        eval = minmax.gameMove.evaluate()
        if eval is not None:
            if eval == 0:
                print("It's a draw!")
            if eval == 1:
                print("Computer won!")
            if eval == -1:
                print("You won!")
            break
