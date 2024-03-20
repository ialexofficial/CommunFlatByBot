import requests
from bs4 import BeautifulSoup as bs
from .parser_base import ParserEngineBase, FlatInfo
from datetime import datetime, timedelta


BASE_URL = "https://infoflat.by/"
TEST_URL = "https://infoflat.by/Home/FlatList?MaxPrice=260&Rooms%5B%5D=1&Rooms%5B%5D=2&Rooms%5B%5D=3&Metro%5B%5D=1-1&Metro%5B%5D=1-2&Metro%5B%5D=1-3&Metro%5B%5D=1-4&Metro%5B%5D=1-5&Metro%5B%5D=1-6&Metro%5B%5D=1-7&Metro%5B%5D=1-8&Metro%5B%5D=1-9&Metro%5B%5D=1-10&Metro%5B%5D=1-11&Metro%5B%5D=1-12&Metro%5B%5D=1-13&Metro%5B%5D=1-14&Metro%5B%5D=1-15&Metro%5B%5D=3-29&IsOwner=true&City=0&_=1710878244228"
URL = "https://infoflat.by/Home/FlatList?MaxPrice=260&Rooms%5B%5D=1&Rooms%5B%5D=2&Rooms%5B%5D=3&Metro%5B%5D=1-1&Metro%5B%5D=1-2&Metro%5B%5D=1-3&Metro%5B%5D=1-4&Metro%5B%5D=1-5&Metro%5B%5D=1-6&Metro%5B%5D=1-7&Metro%5B%5D=1-8&Metro%5B%5D=1-9&Metro%5B%5D=1-10&Metro%5B%5D=1-11&Metro%5B%5D=1-12&Metro%5B%5D=1-13&Metro%5B%5D=1-14&Metro%5B%5D=1-15&Metro%5B%5D=3-29&IsOwner=true&Time=5&City=0"


class InfoflatParserEngine(ParserEngineBase):
    def parse(self, url=URL):
        response = requests.get(url)

        flats = self.parse_html(response.text)

        return flats

    def parse_html(self, text):
        html = bs(text, "html.parser")

        result: list[FlatInfo] = []

        for flat in html.select("div.flats .col-md-12"):
            top_part = flat.div.select_one("a:first-child")
            bottom_part = flat.div.select_one("a:last-child")

            passed_time = timedelta(minutes=int(
                top_part.select_one(".property-location").text.strip()[0]))

            result.append(FlatInfo(
                datetime=datetime.now() - passed_time,
                rooms=bottom_part.select_one(".property-room").text.strip(),
                location=bottom_part.select(
                    ".property-location")[0].text.strip(),
                subway=bottom_part.select(
                    ".property-location")[1].text.strip(),
                price=bottom_part.select_one(".property-price").text.strip(),
                image=flat.select_one("img")["src"],
                url=BASE_URL + flat.select_one("a")["href"],
            ))

        return result


if __name__ == "__main__":
    infoflatParser = InfoflatParserEngine()

    print(*infoflatParser.parse(TEST_URL))
