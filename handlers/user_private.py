from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from filters.chat_types import ChatTypeFilter
from kbds import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник',
                         reply_markup=reply.start_kb3.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Что вас интересует?'
                         ))


@user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
async def menu_command(message: types.Message):
    await message.reply('Вот меню:')


@user_private_router.message(or_f(Command('about'), (F.text.lower() == 'о нас')))
async def about_command(message: types.Message):
    await message.reply('О магазине:')


@user_private_router.message(or_f(Command('payment'), (F.text.lower() == 'варианты оплаты')))
async def payment_command(message: types.Message):
    text = as_marked_section(
        Bold("Варианты оплаты"),  # Bold сделает текст жирным
        "Картой в боте",
        "При получении товара на почте",
        "В заведении",
        marker="✅ "
    )
    await message.reply(text.as_html())


@user_private_router.message((F.text.contains('доставк')) | (F.text.lower() == 'варианты доставки'))  # , озн and
@user_private_router.message(Command('shipping'))
async def shipping_command(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Варианты доставки/заказа"),
            "Курьер",
            "Самовывоз (сейчас прибегу заберу)",
            marker="✅ "
        ),
        as_marked_section(
            Bold("Нельзя"),
            "Почта",
            "Голуби",
            marker="❌ "
        ),
        sep='\n---------------------\n'
    )
    await message.answer(text.as_html())


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f"номер получен")
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f"локация получена")
    await message.answer(str(message.location))
