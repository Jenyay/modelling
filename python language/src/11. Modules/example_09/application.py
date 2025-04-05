# application.py

import tools

if __name__ == "__main__":
    foo = tools.add(10, 20)
    bar = tools.mul(4, 2)
    print("Внутри application.py:", f"{__name__=}")
    print("Внутри application.py:", f"{__file__=}")
    print("Внутри application.py:", f"{tools.__file__=}")
