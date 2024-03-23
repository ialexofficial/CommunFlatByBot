from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup as bs
from .parser_base import ParserEngineBase, FlatInfo, test_parser
from datetime import datetime, timedelta
import re


BASE_URL = "https://infoflat.by/"
URL = "https://infoflat.by/#MaxPrice=260&Rooms%5B%5D=1&Rooms%5B%5D=2&Rooms%5B%5D=3&IsOwner=true&Time=60"


class InfoflatParserEngine(ParserEngineBase):
    async def parse(self, url=URL):
        session = AsyncHTMLSession()

        response = await session.get(url)
        await response.html.arender(timeout=60)

        flats = self.parse_html(response.html.raw_html.decode())

        return flats

    def parse_html(self, text):
        html = bs(text, "html.parser")

        result: list[FlatInfo] = []

        for flat in html.select("div.flats .col-md-12"):
            top_part = flat.div.select_one("a:first-child")
            bottom_part = flat.div.select_one("a:last-child")

            passed_time = timedelta(minutes=int(re.match("^\d+",
                                                         top_part.select_one(".property-location").text.strip())[0]))
            subway = bottom_part.select(".property-location")

            if len(subway) < 2:
                subway = ""
            else:
                subway = subway[1].text.strip()

            result.append(FlatInfo(
                datetime=datetime.now() - passed_time,
                rooms=bottom_part.select_one(".property-room").text.strip(),
                location=bottom_part.select(
                    ".property-location")[0].text.strip(),
                subway=subway,
                price=bottom_part.select_one(".property-price").text.strip(),
                image=flat.select_one("img")["src"],
                url=BASE_URL + flat.select_one("a")["href"],
            ))

        return result


if __name__ == "__main__":
    print(*test_parser(InfoflatParserEngine).send(None))
