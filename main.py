import numpy
import regex as re

class Tree:
    def __init__(self):
        self.root = None

    def merge(self, tree):
        self.root.merge(tree.root)

    def navigate(self, rank):
        nodes = [self.root]
        while len(nodes[-1].children) > 0:
            nodes.append(nodes[-1].clostestChild(rank))

        return [n.move for n in nodes]

    def height(self):
        return root.height()
    def __repr__(self):
        return "Tree(R: " + str(self.root.move) + "/tH: " + str(self.height)+")"

class Node:
    def __init__(self, rank, move, moveNum):
        self.ranks = [rank] #array
        self.move = move
        self.moveNumber = moveNum
        self.children = [] # array

    def height(self):
        childHeights = [c.height() for c in self.children]
        return 1 + max(childHeights)

    def getClostestChild(self, rank):
        clostestChild = self.children[0]
        for c in range(1, len(self.children)):
            if abs(self.children[c].avgRank() - rank) < abs(clostestChild.avgRank() - rank):
                clostestChild = self.children[c]
        return clostestChild

    def avgRank(self):
        return sum(self.ranks) / len(self.ranks)

    def merge(self, node):
        self.ranks += node.ranks
        for self_child in self.children:
            for node_child in node.children:
                if self_child.move == node_child.move:
                    self_child.merge(node_child)

    def __repr__(self):
        return "Node("+str(self.move) + "/tH: " + str(self.height)+")"

class Game:
    def __init__(self):
        self.white = None
        self.black = None
        self.whiteRank = None
        self.blackRank = None
        self.opening = None
        self.moves = None
        self.result = None
        self.winner = None
    def setResult(self, res):
        self.result = res
        w,b = res.split("-")
        w = (int(w.split("/")[0]) / int(w.split("/")[1]) if "/" in w else int(w))
        b = int(b.split("/")[0]) / int(b.split("/")[1]) if "/" in b else int(b)
        if w > b:
            self.winner = "White"
        elif w == b:
            self.winner = "Draw"
        else:
            self.winner = "Black"
    def __repr__(self):
        return self.white+"("+self.whiteRank+") vs " + self.black+"("+self.blackRank+") > "+self.winner

def games_to_trees(gamesList):
    trees = []
    return trees

def mergeAllTrees(treeList):
    tree = treeList[0]
    for t in range(1, len(treeList)):
        tree.merge(treeList[t])
    return tree

def parseFile(input):
    games = []
    with open(input) as f:
        gameObj = None
        for line in f:
            if re.match(r'^\[Event .*', line):
                # print("new Game found")
                gameObj = Game()
            elif re.match(r'^\[White .*', line):
                match = re.match(r'^(?:\[White "(.*)"\])$', line).groups()[0]
                gameObj.white = match
            elif re.match(r'^\[Black .*', line):
                match = re.match(r'^(?:\[Black "(.*)"\])$', line).groups()[0]
                gameObj.black = match
            elif re.match(r'^\[Result .*', line):
                match = re.match(r'^(?:\[Result "(.*)"\])$', line).groups()[0]
                gameObj.setResult(match)
            elif re.match(r'^\[WhiteElo .*', line):
                match = re.match(r'^(?:\[WhiteElo "(.*)"\])$', line).groups()[0]
                gameObj.whiteRank = match
            elif re.match(r'^\[BlackElo .*', line):
                match = re.match(r'^(?:\[BlackElo "(.*)"\])$', line).groups()[0]
                gameObj.blackRank = match
            elif re.match(r'^\[Opening .*', line):
                match = re.match(r'^\[Opening "(.*)"\]$', line).groups()[0]
                gameObj.opening = match
            elif re.match(r'^1. *', line):
                # parse moves
                gameObj.moves = re.findall(r'([1-9][0-9]?\. (?:(?:O-O(?:-0)?)|(?:[KQNBR]?[a-h]?x?[a-h][1-8](?:=[KQNBR])?[\+#]? )){1,2})', line)
                games.append(gameObj)

    return games


def train(dataFiles):
    games = []
    for dataFile in dataFiles:
        games += (parseFile(dataFile))

    print(str(len(games)) + " games parsed successfully")
    #print(games[50])
    #print(games[50].moves)
    return mergeAllTrees(games_to_trees(games))


#only element needed from the game could
def test(tree, avgRank):
    #avgRank = (game.whiteRank + game.blackRank) / 2
    movesList = tree.navigate(avgRank)
    return movesList


def main():
    dataFiles = ["sampleData.pgn"]
    decisionTree = train(dataFiles)
    print(decisionTree)
    test(decisionTree, 555)


main()
