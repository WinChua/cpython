class Tokenizer:
    def __init__(self, tokens):
        self._tokens = tokens

    def __next__(self):
        try:
            return next(self._tokens)
        except StopIteration:
            return None


if __name__ == "__main__":
    t = Tokenizer(i for i in range(10))
    for i in range(13):
        print(next(t))
