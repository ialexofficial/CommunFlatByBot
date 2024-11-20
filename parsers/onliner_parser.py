from bs4 import BeautifulSoup as bs
import time
import datetime
import re

if __name__ == "__main__":
    from parser_base import ParserEngineBase, FlatInfo, test_parser
else:
    from .parser_base import ParserEngineBase, FlatInfo


URL = "https://r.onliner.by/ak/?price%5Bmin%5D=50&price%5Bmax%5D=300&currency=usd&only_owner=true&rent_type%5B%5D=1_room&rent_type%5B%5D=2_rooms&rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms"


class OnlinerParserEngine(ParserEngineBase):
    def parse(self, content: str):
        flats = self.parse_html(content)

        return flats

    def parse_html(self, text) -> list[FlatInfo]:
        html = bs(text, "html.parser")

        result: list[FlatInfo] = []

        def get_text(tag):
            return "" if tag is None else tag.text.strip()

        for flat in html.select("a.classified"):
            image = flat.select_one(".classified__figure img")
            time_text = get_text(flat.select_one(".classified__time")).lower()

            if image is None or ("минут" not in time_text and "час" not in time_text):
                # print(
                # f"Not today {flat['href']} -- Image: {image} -- time_text: {time_text}")
                continue

            # time_text = time_text.removeprefix("Сегодня, ")
            time_group = re.search(r"\d+", time_text)

            if "минут" in time_text:
                time = datetime.timedelta(minutes=int(time_group.group()))
            else:
                time = datetime.timedelta(hours=1 if time_group is None else int(time_group.group()))

            location = get_text(flat.select_one(".classified__caption-item_adress"))
            rooms = get_text(flat.select_one(".classified__caption-item_type"))
            price_rub = get_text(flat.select_one(".classified__price-value.classified__price-value_primary")).replace("\n", "")
            price_usd = get_text(flat.select_one(".classified__price-value.classified__price-value_complementary")).replace("\n", "")

            result.append(FlatInfo(
                datetime=datetime.datetime.now() - time,
                rooms=rooms,
                location=location,
                price=f"{price_rub}/{price_usd}",
                image=image["src"],
                url=flat["href"]
            ))

        return result


if __name__ == "__main__":
    for i in test_parser(OnlinerParserEngine, URL):
        print(i)
