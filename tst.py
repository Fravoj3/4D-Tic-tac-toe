size = 4
def permutate(vec, function, val: list = []):
    if len(val) == size:
        function(val)
        return
    else:
        set_vec = set(vec)
        for i in set_vec:
            copyedVec = vec.copy()
            copyedVec.remove(i)
            copyedVal = val.copy()
            copyedVal.append(i)
            permutate(copyedVec, function, copyedVal)
def addDiagonalLines(vector):
    print(vector)

permutate([1, 1, -1, -1], addDiagonalLines, [])