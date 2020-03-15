import click
from parse import *
from tokenizer import Tokenizer
import re

pattern = re.compile(r"\s*(\w+|--.*|.)")


def tokenizer(buf):
    for line in buf.splitlines():
        for t in pattern.finditer(line.strip()):
            yield t


def genMatch(tokens):
    for token in tokens:
        if token is None:
            return 
        if token.group(1)[:2] == "--":
            continue
        yield token.group(1)

Definition = 0
SumType = 1

@click.command()
@click.option("--filename", default="../asdls/Fig3.asdl", help=u"asdl file to parse")
def p(filename):
    with open(filename) as f:
        buf = f.read()

    tokens = Tokenizer(genMatch(tokenizer(buf)))
    cur_token = next(tokens)
    print(parseModule(cur_token, tokens))

if __name__ == "__main__":
    p()
