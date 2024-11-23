from telebot import TeleBot, types, apihelper
from datetime import datetime, timedelta
from time import sleep
from parsers import parser_base, kufar_parser, onliner_parser
from playwright.sync_api import sync_playwright
import os


TOKEN = "7189321535:AAGFaQuc_4JnG_Lm7VH7ObM7zikJ3A1wPKs"
CHAT = 484336401
SLEEP_TIME_MINUTES = 5

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    print(message.chat)

    bot.send_message("I'm not ready")


def send_flats(flats: list[parser_base.FlatInfo]):
    for flat in flats:
        try:
            bot.send_photo(
                CHAT,
                flat.image,
                caption=flat.format_caption(),
                parse_mode="markdown"
            )
        except apihelper.ApiTelegramException as e:
            try:
                bot.send_message(CHAT, flat.format_caption(),
                                 parse_mode="markdown")
            except apihelper.ApiTelegramException as e:
                print("-------------------")
                print(f"{e.function_name} -- {e.description}")
                print(flat.format_caption())
                print("-------------------")


def main():
    # bot.infinity_polling()
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)

    kufar = parser_base.FlatParser(
        kufar_parser.KufarParserEngine, kufar_parser.URL, browser.new_page())
    onliner = parser_base.FlatParser(
        onliner_parser.OnlinerParserEngine, onliner_parser.URL, browser.new_page())

    deltatime = timedelta(minutes=SLEEP_TIME_MINUTES + 2)

    while True:
        flats = kufar.parse(deltatime) + onliner.parse(deltatime)

        print(f"New flats: {datetime.now()} -- {len(flats)}")
        send_flats(flats)

        sleep(SLEEP_TIME_MINUTES * 60)


if __name__ == "__main__":
    version_tag = os.environ.get(key="APP_VERSION_TAG")

    print(f"Hello from CommunFlatByBot{f":{version_tag}" if version_tag is not None else ""}")

    # bot.send_message(CHAT, "Hello from infoflatbyBot")

    main()
