class Example:
    _x: int = 1

    @classmethod
    @property
    def x(cls) -> int:
        return cls._x


def func(val: int):
    print(val)


func(Example.x)  # type: ignore
