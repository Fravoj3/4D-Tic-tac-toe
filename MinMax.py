'''
MinMax algorithm for AI player.
'''

class MinMax:
    class GameBoard:
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


        def __init__(self, size, board=None):
            self.size = size
            if board is None:
                self.board = [[[[ MinMax.GameBoard.Point() for i in range(size)] for j in range(size)] for k in range(size)] for l in range(size)]
            else:
                self.board = board

        def copyBoard(self):
            newBoard = [[[[self.board[l][k][j][i] for i in range(self.size)] for j in range(self.size)] for k in range(self.size)] for l in range(self.size)]
            return MinMax.GameBoard(3, newBoard)
        
        @staticmethod
        def setPoint(x, y, z, w, player, board):
            '''
            Sets point on the board representing player's move. x, y, z, w, are coordinates of player on given board.
            returns True if player has won in axis x, y, z or w (exceot body diagonals).
            '''
            board = board.board

            def getNeighbourVal(x, y, z, w, dir):
                if x < 0 or y < 0 or z < 0 or w < 0:
                    return 0
                if x >= len(board) or y >= len(board) or z >= len(board) or w >= len(board):
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
                if x >= len(board) or y >= len(board) or z >= len(board) or w >= len(board):
                    return

                for i in range(2):
                    shift = 0
                    while True:
                        if dir == 'x':
                            if x+shift >= len(board) or x+shift < 0:
                                break
                            if board[x+shift][y][z][w].player != player:
                                break
                            board[x+shift][y][z][w].neighboursOnX = val
                        if dir == 'y':
                            if y+shift >= len(board) or y+shift < 0:
                                break
                            if board[x][y+shift][z][w].player != player:
                                break
                            board[x][y+shift][z][w].neighboursOnY = val
                        if dir == 'z':
                            if z+shift >= len(board) or z+shift < 0:
                                break
                            if board[x][y][z+shift][w].player != player:
                                break
                            board[x][y][z+shift][w].neighboursOnZ = val
                        if dir == 'w':
                            if w+shift >= len(board) or w+shift < 0:
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
                
        @staticmethod
        def evaluate(board):
            '''
            Evaluates board state. Returns player who has won or -1 if no one has won.
            '''
            won = [None, False, False]
            for i in range(len(board)):
                for j in range(len(board)):
                    for k in range(len(board)):
                        for l in range(len(board)):
                            if board[i][j][k][l].neighboursOnX >= 3:
                                won[board[i][j][k][l].player] = True
                            if board[i][j][k][l].neighboursOnY >= 3:
                                won[board[i][j][k][l].player] = True
                            if board[i][j][k][l].neighboursOnZ >= 3:
                                won[board[i][j][k][l].player] = True
                            if board[i][j][k][l].neighboursOnW >= 3:
                                won[board[i][j][k][l].player] = True
                        
            def diagonalCheck(start, shift):
                for i in range(len(board)):
                    if board[start[0]+i*shift[0]][start[1]+i*shift[1]][start[2]+i*shift[2]][start[3]+i*shift[3]].player != board[start[0]][start[1]][start[2]][start[3]].player:
                        return False
                    
                won[board[start[0]][start[1]][start[2]][start[3]].player] = True

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

    class State:
        def __init__(self, board, player):
            self.board = board
            self.player = player
            self.state = MinMax.GameBoard.evaluate(board.board) # whether someone has won
            self.value = None # value of the state in case of limited depth
            self.children = dict()

    def __init__(self, size, depth=None, startingPlayer=1):
        self.size = size
        self.depth = depth
        self.startingPlayer = startingPlayer

    def startMinMax(self):
        state = MinMax.State(MinMax.GameBoard(self.size), self.startingPlayer)
        winner = self.minMax(state, -1, 1)
        return state

    def minMax(self, state, alpha, beta):
        if state.state is not None:
            return state.state

        value = None
        shouldBreak = False
        # generate all possible moves
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    for l in range(self.size):
                        if state.board.board[i][j][k][l].player == 0:
                            newBoard = state.board.copyBoard()
                            MinMax.GameBoard.setPoint(i, j, k, l, state.player, newBoard)
                            
                            newState = MinMax.State(newBoard, 1 if state.player == 2 else 2)
                            state.children[f'{i}.{j}.{k}.{l}'] = newState
                            val = self.minMax(newState, alpha, beta)

                            if state.player == 1:
                                if value is None or val > value:
                                    value = val
                            else:
                                if value is None or val < value:
                                    value = val
                            state.value = value

                            # if state.player == 1:
                            #     if val > alpha:
                            #         alpha = val
                            # else:
                            #     if val < beta:
                            #         beta = val
                            # if alpha >= beta:
                            #     shouldBreak = True
                            #     break
        #             if shouldBreak:
        #                 break
        #         if shouldBreak:
        #             break
        #     if shouldBreak:
        #         break
        print(state.children)
        return value

    def computeTree(self):
        self.tree = self.startMinMax()

    def restartGame(self):
        if self.tree is None:
            Exception('Tree not computed')

        self.gameState = self.tree

    def makeMove(self, move):
        index = f"{move[0]}.{move[1]}.{move[2]}.{move[3]}"
        if index not in self.gameState.children:
            print("invalid move")
            for key in self.gameState.children.keys():
                print(key)
            Exception('Invalid move')
        self.gameState = self.gameState.children[index]
    
    def getAndMakeBestMove(self):
        if self.tree is None:
            Exception('Tree not computed')

        bestMove = None
        bestValue = None
        for key, val in self.gameState.children.items():
            if bestValue is None or val.value > bestValue:
                bestValue = val.value
                bestMove = key

        self.gameState = self.gameState.children[bestMove]
        return [int(i) for i in bestMove.split('.')]

    def isGameFinished(self):
        if len(self.gameState.children) == 0:
            return self.gameState.state

if __name__	== '__main__':
    minMax = MinMax(3, startingPlayer=2)
    minMax.computeTree()
    minMax.restartGame()
    print(minMax.tree.children)
    start = int(input("0 - you start, 1 - AI starts"))
    player = start

    while True:
        finished = minMax.isGameFinished() 
        if finished is not None:
            if finished == 0:
                print("Draw")
            if (finished == -1 and start == 0) or (finished == 1 and start == 1):
                print("You won")
            else:
                print("AI won")
            break

        if player == 0:
            print("Enter move: ")
            x, y, z, w = [int(i) for i in input().split()]
            minMax.makeMove([x, y, z, w])
            player = 1
        else:
            move = minMax.getAndMakeBestMove()
            print(move)
            player = 0


