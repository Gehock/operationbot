import asyncio
import logging
import sys
from typing import Optional, Tuple

# from discord.emoji import Emoji


class Emoji:
    pass


class Type:
    def __eq__(self, o: object) -> bool:
        print(f"{o=} {type(o)=}")
        return True


class Database:
    _value: Optional[Tuple[Emoji, ...]] = None
    data = 1

    @classmethod
    def change_data(cls, data):
        cls.data = data

    @classmethod
    def load_data(cls, data=None):
        print(f"{cls.__name__} load")
        cls._value = data

    @classmethod
    # @staticmethod
    @property
    def value(cls) -> Tuple[Emoji, ...]:
        print(f"{cls.__name__} property")
        if cls._value is None:
            raise ValueError("Value not set")
        return cls._value

    @classmethod
    async def create_item_async(cls):
        print(f"{cls.__name__} create async")
        for x in cls.value:  # hint: ignore
            print(f"{cls.__name__} {x=}")
        Item(cls.value, f"{cls.__name__}")  # hint: ignore

    @classmethod
    def create_item(cls):
        print(f"{cls.__name__} create")
        # for x in cls.value:
        #     print(f"{cls.__name__} {x=}")
        Item(cls.value, f"{cls.__name__}")  # hint: ignore


class Item:
    def __init__(self, value: Tuple[Emoji, ...], classname) -> None:
        self._print(value, classname)

    def _print(self, value: Tuple[Emoji, ...], classname):
        print(f"it {classname} {value=}")
        for x in value:
            print(f"it {classname} {x=}")


class DB2(Database):
    # @classmethod
    # def set_value(cls):
    #     cls._value = [3,4,5]

    @classmethod
    def load_data(cls, data=None):
        print(f"{cls.__name__} load")
        cls._value = data  # or [4,5,6]


async def do_async():
    # Should raise an error
    # await Database.create_item_async()
    Database.load_data()
    # Should print the value
    await Database.create_item_async()


def do():
    if Database.value is None:
        print("it's none")
    # Should raise an error
    # try:
    #     Database.create_item()
    # except ValueError:
    #     print("ValueError")
    # Database.load_data()
    # # Should print the value
    # Database.create_item()
    # DB2.load_data()
    # Database.create_item()
    # DB2.create_item()
    # print(f"{Database.data=}")
    # Database.data = 2
    # print(f"{Database.data=}")
    # DB2.data = 3
    # print(f"{Database.data=}")
    # print(f"{DB2.data=}")
    # Database.change_data(4)
    # print(f"{Database.data=}")
    # print(f"{DB2.data=}")


if __name__ == "__main__":
    if sys.version_info < (3, 9):
        raise ValueError("Must be run with Python 3.9 or higher")
    if len(sys.argv) > 1 and sys.argv[1] == "async":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(do_async())
        # asyncio.run(do_async())
    else:
        # do()
        pass

    try:
        raise ValueError("Test")
    except ValueError:
        logging.exception("Error occured")
