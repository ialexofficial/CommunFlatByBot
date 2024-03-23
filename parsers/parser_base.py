import abc
from datetime import datetime, timedelta


class FlatInfo:
    def __init__(
        self,
        datetime: datetime,
        rooms: str,
        location: str,
        price: str,
        image: str,
        url: str,
        subway: str = ""
    ):
        self.datetime = datetime
        self.rooms = rooms
        self.location = location
        self.price = price
        self.image = image
        self.url = url
        self.subway = subway

    def format_caption(self) -> str:
        return (
            f"*{self.rooms}*\n" +
            f"{self.location}" +
            (f", _{self.subway}_\n" if self.subway != "" else "\n") +
            f"*{self.price}*, {self.datetime.strftime('%H:%M')}\n" +
            f"{self.url}"
        ).replace("*", "")

    def __str__(self):
        return self.format_caption()


class ParserEngineBase(abc.ABC):
    @abc.abstractmethod
    async def parse(self, url: str) -> list[FlatInfo]:
        ...


class FlatParser():
    def __init__(self, engine_class: type[ParserEngineBase], parsing_url: str):
        self.__engine = engine_class()
        self.__url = parsing_url

    async def parse(self, deltatime: timedelta) -> list[FlatInfo]:
        flats = await self.__engine.parse(self.__url)

        return [f for f in flats if datetime.now() - f.datetime < deltatime]


async def test_parser(engine: type[ParserEngineBase], url: str) -> list[FlatInfo]:
    return await FlatParser(engine, url).parse(timedelta.max)
