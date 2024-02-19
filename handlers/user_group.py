from string import punctuation

from aiogram import types, Router, F

from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'кабан', 'хомяк', 'выхухоль'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))
# убираем знаки пунктуации чтобы не маскировали слова


# если пользователь отредактирует свой текс на запрещенные слова чтобы мы их тоже отлавливали
@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.first_name}, соблюдайте порядок в чате!")
        await message.delete()

        # await message.chat.ban(message.from_user.id)
