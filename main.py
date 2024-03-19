from telebot import TeleBot, types, apihelper
from time import sleep
from datetime import datetime
from site_parser import parse, TEST_URL


TOKEN = "7189321535:AAGFaQuc_4JnG_Lm7VH7ObM7zikJ3A1wPKs"
CHAT = 484336401
SLEEP_TIME = 5 * 60

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    print(message.chat)

    bot.send_message("I'm not ready")


def format_caption(flat: dict[str, str]):
    return (
        f"*{flat['rooms']}*\n" +
        f"{flat['location']}, _{flat['subway']}_\n" +
        f"*{flat['price']}*, {flat['time']}\n" +
        f"{flat['url']}"
    )


def send_flats(flats: list[dict[str, str]]):
    for flat in flats:
        caption = format_caption(flat)

        try:
            bot.send_photo(
                CHAT,
                flat["image"],
                caption=caption,
                parse_mode="markdown"
            )
        except apihelper.ApiTelegramException as e:
            try:
                bot.send_message(CHAT, caption, parse_mode="markdown")
            except apihelper.ApiTelegramException as e:
                print(f"{e.description} -- {flat['url']}")


def main():
    # bot.infinity_polling()

    while True:
        flats = parse()

        print(f"{datetime.now()} -- {len(flats)}")
        send_flats(flats)

        sleep(SLEEP_TIME)


if __name__ == '__main__':
    print("Hello from infoflatbyBot")

    bot.send_message(CHAT, "Hello from infoflatbyBot")

    main()
