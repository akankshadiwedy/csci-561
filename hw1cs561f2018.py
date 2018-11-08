from Queue import PriorityQueue
import time

class Node():
    def __init__(self,value,parent,children):
        self.value = value
        self.parent = parent
        self.children = children

class tree():
    def __init__(self):
        self.root = Node('INITIALSTATE','Null',{})
        self.nodeList = [self.root]

    def addNode(self,parent,value,edgeCost):
        self.childNode = Node(value,parent,{})
        parent.children[self.childNode] = edgeCost
        self.nodeList.append(self.childNode)

    def getNode(self,value):
        for node in self.nodeList:
            if node.value == value:
                return node

def goalTest(officerPlaced,officerCount):
    if officerPlaced == officerCount:
        return True
    else:
        return False

def findChildren(path,scooterPositionsCount,gridSize):
    parent = path[-1].split(',')
    parentX,parentY = int(parent[0]),int(parent[1])
    for i in range(gridSize):
        for j in range(gridSize):
            validPositions[i][j] = True
    for pos in path:
        xy=pos.split(',')
        x,y = int(xy[0]),int(xy[1])
        validPositions[x][y] = False
        for i in range(gridSize):
            for j in range(gridSize):
                if i==x or j==y or abs(i-x) == abs(j-y):
                    validPositions[i][j]= False
                if scooterPositionsCount[i][j] > scooterPositionsCount[parentX][parentY]:
                    validPositions[i][j] = False


def UCS(scooterPositionsCount,officerCount,gridSize):
    maxCostStack = PriorityQueue()
    maxCost = 0
    while not frontier.empty():
        if (time.time() - start) < 175:
            node = frontier.get()
            #print 'path : ', node[1], 'currMAXCOST : ',maxCost
            if (node[0]* (-1)) > maxCost:
                maxCost = node[0] * (-1)
                maxCostStack.put(maxCost * (-1))
            if node[2] < maxCost: # deletes all paths having maximum possible activity points less than activity points already received in different path
                if (node[0] * (-1)) == maxCost:
                    maxCostStack.get()
                    newMaxCost = maxCostStack.get()
                    maxCost = newMaxCost * (-1)
                    maxCostStack.put(newMaxCost)
                    continue
            else:
                traversedPath = node[1].split('->')
                traversedPath.remove('INITIALSTATE')
                officerPlaced = len(traversedPath)
                #print node[0]
                if officerCount == 1:
                    goalsReached.put(node)
                    continue
                else:
                    findChildren(traversedPath,scooterPositionsCount,gridSize)
                    isChildrenPresent = False
                    for i in range(gridSize):
                        for j in range(gridSize):
                            if validPositions[i][j] == True:
                                isChildrenPresent = True
                                child = str(i)+','+str(j)
                                ap = node[0] - scooterPositionsCount[i][j]
                                possibleCost = (scooterPositionsCount[i][j] * (officerCount - officerPlaced)) + (
                                            node[0] * (-1))
                                if goalTest(officerPlaced + 1, officerCount):
                                    goalsReached.put((ap, node[1] + '->' + child))
                                else:
                                    frontier.put((ap, node[1] + '->' + child, possibleCost))
                    if isChildrenPresent == False:
                        if (node[0] * (-1)) == maxCost:
                            maxCostStack.get()
                            newMaxCost = maxCostStack.get()
                            maxCost = newMaxCost * (-1)
                            maxCostStack.put(newMaxCost)
                        continue
        else:
            return
    return


lines = [line.rstrip() for line in open("input.txt")]
scooterPositions = []
gridSize = 0
officerCount = 0
scooterCount = 0
lineCount = 0
goalsReached = PriorityQueue()
for line in lines:
    lineCount += 1
    if(lineCount == 1):
        gridSize = int(line)
        scooterPositionsCount = [[0] * gridSize for c in range(gridSize)]
        validPositions = [[0] * gridSize for c in range(gridSize)]
    elif(lineCount == 2):
        officerCount = int(line)
    elif(lineCount == 3):
        scooterCount = int(line)
    else:
        scooterPositions.append(line)
        position = line.split(',')
        x,y=int(position[0]),int(position[1])
        scooterPositionsCount[x][y] += 1

#scooterPositionsCount = [[0] * gridSize for c in range(gridSize)]
#validPositions = [[0] * gridSize for c in range(gridSize)]
#scooterPositionsCount = [[16, 42, 27, 6, 37, 5, 8, 0, 0, 2, 48, 12, 23, 13], [16, 2, 28, 14, 21, 1, 4, 37, 5, 15, 31, 21, 16, 42], [5, 28, 5, 40, 45, 13, 36, 41, 33, 48, 31, 22, 15, 9], [5, 1, 34, 44, 16, 39, 9, 21, 42, 4, 45, 2, 0, 22], [11, 50, 6, 37, 46, 34, 37, 24, 8, 26, 44, 35, 25, 2], [45, 17, 1, 25, 23, 45, 17, 23, 23, 26, 40, 49, 3, 2], [6, 39, 34, 41, 22, 19, 31, 45, 11, 20, 3, 41, 33, 3], [2, 50, 11, 27, 1, 29, 21, 19, 14, 0, 2, 30, 35, 40], [3, 39, 28, 5, 2, 9, 27, 37, 43, 20, 35, 1, 11, 23], [18, 18, 30, 39, 34, 19, 39, 21, 45, 1, 33, 36, 36, 1], [28, 7, 32, 19, 4, 39, 19, 15, 15, 20, 28, 12, 15, 5], [7, 50, 33, 42, 32, 2, 35, 24, 36, 49, 35, 11, 17, 13], [1, 48, 5, 37, 17, 3, 30, 2, 44, 25, 0, 8, 24, 47], [43, 46, 6, 28, 15, 2, 40, 45, 39, 35, 23, 26, 14, 23]]

#print scooterPositionsCount

frontier = PriorityQueue()
for i in range(gridSize):
    for j in range(gridSize):
        position = str(i)+','+str(j)
        possibleCost = scooterPositionsCount[i][j] * officerCount
        frontier.put(((scooterPositionsCount[i][j] * (-1)),'INITIALSTATE' + '->' + position, possibleCost))
start = time.time()
UCS(scooterPositionsCount,officerCount,gridSize)
goal = goalsReached.get()
ActivityPoints = str(goal[0]*(-1))
#print ActivityPoints
myOutput = open("output.txt", "w+")
myOutput.write(str(ActivityPoints))