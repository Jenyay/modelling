import mymath.actions
import mymath.equations

if __name__ == "__main__":
    foo = mymath.actions.add(10, 20)
    bar = mymath.actions.mul(4, 2)
    result = mymath.equations.equation(5, 2, -10)

    print(f"{type(mymath)=}")
    print(f"{type(mymath.actions)=}")
    print(f"{type(mymath.equations)=}")
