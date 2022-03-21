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



def main():
    inputFile = "sampleData.pgn"
    games = parseFile(inputFile)
    print(str(len(games)) + " games parsed successfully")
    print(games[0])

def parseFile(input):
    games = []
    with open(input) as f:
        gameObj = None
        for line in f:
            if re.match(r'^\[Event .*', line):
                games.append(gameObj)
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
                gameObj.result = match
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
                matches = re.match(r'^(?:\d\. (.*))$', line).groups()
                gameObj.opening = match
    return games

main()
