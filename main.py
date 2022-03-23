import numpy
import regex as re

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

def main():
    inputFile = "sampleData.pgn"
    games = parseFile(inputFile)
    print(str(len(games)) + " games parsed successfully")
    print(games[50])


main()
