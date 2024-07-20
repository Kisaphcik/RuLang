import sys
from myPylexer import Lexer
from myPyParser import Parser

if __name__ == "__main__":
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            lexer = Lexer((file.read()))
    except IndexError:
        with open("main.rl", 'r', encoding='utf-8') as file:
            lexer = Lexer((file.read()))
    finally:
        parser = Parser(lexer.tokensList)