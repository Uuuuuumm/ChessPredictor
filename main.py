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
			nodes.append(nodes[-1].getClostestChild(rank))

		return [n.move for n in nodes]

	def height(self):
		return self.root.height()

	def worse_height(self):
		node = self.root
		height = 0
		while node is not None:
			node = node.children[0]
			height = height + 1

		return height

	def __repr__(self):
		# return "Tree(R: " + str(self.root.move) + ", C: " + str(len(self.root.children))+")"
		return "Tree(R: " + str(self.root.move) + ", H: " + str(self.height())+", C: " + str(len(self.root.children))+")"
		# return "Tree(R: " + str(self.root.move) + "/tH: " + str(self.worse_height)+")"

class Node:
    def __init__(self, rank, move):
        self.ranks = [rank] #array
        self.move = move
        #self.moveNumber = moveNum
        self.children = [] # array

    def height(self):
        childHeights = [c.height() for c in self.children]
        if len(childHeights) == 0:
            return 1
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

        for node_child in node.children:
            hasNode = False
            for self_child in self.children:
                if self_child.move == node_child.move:
                    hasNode = True

            if not hasNode:
                self.children.append(node_child)

    def __repr__(self):
        return "Node("+str(self.move) + "/tH: " + str(self.height)+")"

    def print(self):
        print(self.move)
        for c in self.children:
            c.print()

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

def games_to_trees(gamesList, numTurns):

    trees = []

    for game in gamesList:
        # if not ("e4" in game.moves[0]):
        #     continue

        if len(game.moves) >= numTurns:
            tree = Tree() 	# create a tree for this game
            # create list of moves
            moves = game.moves
            whiteRank = game.whiteRank
            blackRank = game.blackRank

            # to keep track of where to attach new nodes
            parentNode = None

            for i in range(numTurns):

                if parentNode is None and i > 0:
                    break

                # have to create two nodes for every move for white and black
                whiteNode = Node(whiteRank, moves[i].split(" ")[1])#, i)

                # last move may be by white
                blackNode = None
                #blackNode = Node()
                if len(moves[i].split(" ")) == 4:
                    blackNode = Node(blackRank, moves[i].split(" ")[2])#, i+1)
                # print(len(moves[i].split(" ")))
                if i == 0:
                    tree.root = whiteNode
                    # if blackNode is None:
                    #     break
                    # whiteNode.children.append(blackNode)
                    # parentNode = blackNode
                else:
                    parentNode.children.append(whiteNode)

                if blackNode is None:
                    break
                whiteNode.children.append(blackNode)
                parentNode = blackNode

            trees.append(tree) # add tree to list of trees

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
        gameValid = True
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
                if match == "?":
                    gameValid = False
                else:
                    gameObj.whiteRank = int(match)
            elif re.match(r'^\[BlackElo .*', line):
                match = re.match(r'^(?:\[BlackElo "(.*)"\])$', line).groups()[0]
                if match == "?":
                    gameValid = False
                else:
                    gameObj.blackRank = int(match)


            elif re.match(r'^\[Opening .*', line):
                match = re.match(r'^\[Opening "(.*)"\]$', line).groups()[0]
                gameObj.opening = match
            elif re.match(r'^1. *', line):
                # parse moves
                gameObj.moves = re.findall(r'([1-9][0-9]?\. (?:(?:O-O(?:-0)?)|(?:[KQNBR]?[a-h]?x?[a-h][1-8](?:=[KQNBR])?[\+#]? )){1,2})', line)
                if gameValid:
                    games.append(gameObj)
                gameValid = True

    return games


def train(dataFiles, numTurns):
    games = []
    for dataFile in dataFiles:
        games += (parseFile(dataFile))

    print(str(len(games)) + " games parsed successfully")
    trees = games_to_trees(games, numTurns)
    # for i in range(0, 10):
    #     print(trees[i])
    return mergeAllTrees(trees)


#only element needed from the game could
def test(tree, avgRank):
	#avgRank = (game.whiteRank + game.blackRank) / 2
	movesList = tree.navigate(avgRank)
	return movesList


def main():
    dataFiles = ["sampleData.pgn", "trainingData/td1.pgn"]
    decisionTree = train(dataFiles, 2)
    # decisionTree.root.print()

    print(decisionTree)
    # print(decisionTree.root)
    # print(decisionTree.root.children[0])
    moveList = test(decisionTree, 1200)
    print(moveList)


main()
