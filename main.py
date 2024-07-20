import sys
from myPylexer import Lexer
from myPyParser import Parser

if __name__ == "__main__":
    with open("main.rl", 'r', encoding='utf-8') as file:
            mylexer = Lexer(file.read())
    parser = Parser(mylexer.tokensList)