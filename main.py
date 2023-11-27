from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from mem_generator import MemeGenerator
from config import token
import traceback
import io

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'], )
async def send_welcome(msg: types.Message):
    print('in send_welcome')
    await msg.answer('Hello!')

@dp.message_handler(commands=['menu', 'help'], )
async def send_menu(msg: types.Message):
    await msg.answer('Существуют команды: start, menu, help, sum')

@dp.message_handler(commands=['sum'], )
async def send_sum(msg: types.Message):
    a, b, c = msg.text.split()
    print(a, b, c)
    await msg.answer(f"answer: {int(b) + int(c)}")

@dp.message_handler(commands=['generate'], )
async def meme_generate(msg: types.Message):
    try:
        cmd, name, *arg = msg.text.split()
        #MemeGenerator.save_meme_to_disk(name, "C:/Users/ВАГИЗ/Desktop/projects/tg_bot", arg )
        arg1 = ""
        for i in range(len(arg)):
            arg1 = arg[i].replace('_', ' ')
            arg[i] = arg1
        meme_pill = MemeGenerator.get_meme_image(name, arg)
        output = io.BytesIO()
        meme_pill.save(output, format='png')

        await bot.send_photo(msg.from_user.id, photo=output.getvalue(),
                                caption=f'Meme {name}')
    except:
        print(traceback.format_exc())
    #new
@dp.message_handler(commands=['c'], )
async def send_c(msg: types.Message):
    if len(msg.text.split()) == 4:  
        y, a, operator, c = msg.text.split()
        if is_number(a) == True and is_number(c) == True:
            a = int(a)
            c = int(c)
            if operator =='+':
                otvet = a + c
            elif operator == '-':
                otvet = a - c
            elif operator == '*':
                otvet = a * c
            elif operator == ':':
                otvet = a / c
            else:
                otvet = 'допустимые знаки: "+", "-", "*", ":".'
            await msg.answer(otvet)
        else:
            await msg.answer("вы ввели не число")
    else:
        await msg.answer("допустимый формат сообщения: /c число знак число \n пример:/c 4 * 5")
    #new
def is_number(msg: str) -> bool:
    '''
        возращает  true если  msg  число иначе false
    '''
    for i in msg:
        if i.isdigit() == True:
            continue
        else:
            return False
    return True
executor.start_polling(dp)

