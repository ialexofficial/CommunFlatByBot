import abc
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright, Page


RELOAD_TIMEOUT = 90_000


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
    def parse(self, page_content: str) -> list[FlatInfo]:
        ...


class FlatParser():
    def __init__(self, engine_class: type[ParserEngineBase], parsing_url: str, page: Page):
        self.__engine = engine_class()
        self.__url = parsing_url
        self.__page = page
        self.__page.goto(self.__url)

    def parse(self, deltatime: timedelta) -> list[FlatInfo]:
        self.__page.reload(timeout=RELOAD_TIMEOUT)
        self.__page.wait_for_load_state("networkidle")

        flats = self.__engine.parse(self.__page.content())

        return [f for f in flats if datetime.now() - f.datetime < deltatime]


def test_parser(engine: type[ParserEngineBase], url: str) -> list[FlatInfo]:
    return FlatParser(engine, url).parse(timedelta.max)
