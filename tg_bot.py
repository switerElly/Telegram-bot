import logging
import shelve
import time

from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, executor, types

TOKEN = "5942791567:AAH9smBOYzYYguVT9XsMuwaiBxLlqXZVqjw"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

users: list[str] = list()
timing: list[str] = list()


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id_name = f'{message.from_user.id}_{message.from_user.first_name}'
    current_time = time.strftime("%d.%m.%Y %H-%M", time.localtime(time.time()))
    global person
    tmp = 0
    for per in users:
        if per == user_id_name:
            tmp += 1
            person = per
            break
    if tmp == 0:
        users.append(user_id_name)
        timing.append(current_time)
    else:
        timing[users.index(person)] = current_time
    im = Image.open(r"C:\Users\2020\PycharmProjects\cat.jpg")
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (370, 470),
        time.strftime("%d.%m.%Y %H-%M", time.localtime(time.time())),
        font=ImageFont.truetype("arial.ttf", 50),
        fill="#560319")
    im.save(r'C:\Users\2020\PycharmProjects\newcat.jpg')
    photo = open(r"C:\Users\2020\PycharmProjects\newcat.jpg", 'rb')
    await bot.send_photo(message.from_user.id, photo)


if __name__ == "__main__":
    executor.start_polling(dp)
    db = shelve.open("bot.db")
    for i in range(len(users)):
        db[f'user_{i}'] = {users[i]: timing[i]}
        print(db[f'user_{i}'])
    db.close()
