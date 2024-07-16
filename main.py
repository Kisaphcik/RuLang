import sys
from myPylexer import Lexer
from myPyParser import Parser

if __name__ == "__main__":
    with open("main.rl", 'r', encoding='utf-8') as file:
        lexer = Lexer((file.read()))
    parser = Parser(lexer.tokensList)