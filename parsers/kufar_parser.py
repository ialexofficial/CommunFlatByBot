from requests_html import AsyncHTMLSession
from .parser_base import ParserEngineBase, FlatInfo, test_parser
from bs4 import BeautifulSoup as bs
from datetime import time, datetime

URL = "https://re.kufar.by/l/minsk/snyat/kvartiru-dolgosrochno/bez-posrednikov?cur=USD&prc=r%3A0%2C260&size=30"


class KufarParserEngine(ParserEngineBase):
    async def parse(self, url=URL):
        session = AsyncHTMLSession()

        response = await session.get(url)
        await response.html.arender(timeout=60)

        flats = self.parse_html(response.html.raw_html.decode())

        return flats

    def parse_html(self, text) -> list[FlatInfo]:
        html = bs(text, "html.parser")

        result: list[FlatInfo] = []

        def check_for_class_substr(class_, substr: str) -> bool:
            return False if class_ is None else substr in class_

        def get_text(tag):
            return "" if tag is None else tag.text.strip()

        for flat in html.select("section a"):
            image = flat.select_one(".swiper-slide img")
            time_text = get_text(
                flat.find("div", class_=lambda c: check_for_class_substr(c, "_date_")))

            if image is None or "Сегодня" not in time_text:
                # print(
                # f"Not today {flat['href']} -- Image: {image} -- time_text: {time_text}")
                continue

            time_text = time_text.removeprefix("Сегодня, ")

            location = flat.find(
                "div", class_=lambda c: check_for_class_substr(c, "_address"))

            result.append(FlatInfo(
                datetime=datetime.combine(
                    datetime.now().date(), time.fromisoformat(time_text)),
                rooms=get_text(
                    flat.find("div", class_=lambda c: check_for_class_substr(c, "_parameters_"))),
                location=get_text(location),
                subway=get_text(location.nextSibling),
                price=get_text(flat.find("span", class_=lambda c: check_for_class_substr(c, "_price__byr"))) +
                "/" +
                get_text(
                    flat.find("span", class_=lambda c: check_for_class_substr(c, "_price__usd"))),
                image=image["src"],
                url=flat["href"]
            ))

        return result


if __name__ == "__main__":
    print(*test_parser(KufarParserEngine, URL))
