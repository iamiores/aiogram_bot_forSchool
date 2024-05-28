from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import os

from app.keyboards import *
from text import *
from config import ADMIN_LAW_USER_ID, ADMIN_TECH_USER_ID
from bot import bot

router = Router()


class Form(StatesGroup):
    main_state = State()
    vpo_state = State()
    military_state = State()
    war_victims_state = State()
    support_state = State()
    awaiting_question_tech = State()
    awaiting_question_law = State()


user_message_mapping_tech = {}
user_message_mapping_law = {}


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(start_txt, reply_markup=main)
    await state.set_state(Form.main_state)


# SUPPORT
@router.message(F.text == "Зворотній зв'язок")
async def process_support(message: Message, state: FSMContext):
    await message.answer(text='Виберіть опцію', reply_markup=support)
    await state.set_state(Form.support_state)


@router.message(F.text == 'Технічна підтримка')
async def tech_support(message: Message, state: FSMContext):
    if message.from_user.id == int(ADMIN_TECH_USER_ID):
        await message.reply('Вибач, ти не можеш надсилати повідомлення самому собі:(', reply_markup=main)
        return
    else:
        await message.answer('Надішліть ваше питання.')

    async def forward_to_tech_admin(message: Message):
        if message.from_user.id != int(ADMIN_TECH_USER_ID):
            forward_message = await bot.send_message(ADMIN_TECH_USER_ID, f'{message.from_user.first_name}\n{message.from_user.username}\n{message.text}')
            user_message_mapping_tech[forward_message.message_id] = message.from_user.id
            await message.answer('Ваше повідомлення було надіслано.', reply_markup=main)
            # print(forward_message.message_id)
        else:
            if message.reply_to_message and message.reply_to_message.message_id:
                message_id = message.reply_to_message.message_id
                if message_id in user_message_mapping_tech.keys():
                    user_id = user_message_mapping_tech[message_id]
                    await bot.send_message(user_id, f'Відповідь:\n{message.text}')
                    await bot.send_message(chat_id=ADMIN_TECH_USER_ID, text='Відповідь була надіслана.')
                    await state.clear()
                else:
                    await message.answer('Користувача не знайдено.')
                    # print(message_id)
            else:
                await message.answer('Відповідайте на повідомлення користувача, щоб відправити відповідь.')

    if message.reply_markup is not None:
        await forward_to_tech_admin(message)
        await state.clear()
    else:
        await state.set_state(Form.awaiting_question_tech.state)

        async def check_for_question_tech(message: Message):
            check_state = await state.get_state()
            if check_state == Form.awaiting_question_tech.state:
                await forward_to_tech_admin(message)

        @router.message()
        async def forward_message_tech_handler(message: Message):
            await check_for_question_tech(message)


@router.message(F.text == 'Потрібне уточнення')
async def law_support(message: Message, state: FSMContext):
    if message.from_user.id == int(ADMIN_LAW_USER_ID):
        await message.reply('Вибач, ви не можете надсилати повідомлення самому собі:(', reply_markup=main)
        return
    else:
        await message.answer('Надішліть ваше питання.')

    async def forward_to_law_admin(message: Message):
        if message.from_user.id != int(ADMIN_LAW_USER_ID):
            forward_message = await bot.send_message(ADMIN_LAW_USER_ID, f'{message.from_user.first_name}\n{message.from_user.id}\n{message.text}')
            user_message_mapping_law[forward_message.message_id] = message.from_user.id
            await message.answer('Ваше повідомлення було надіслано.', reply_markup=main)
            # print(forward_message.message_id)
        else:
            if message.reply_to_message and message.reply_to_message.message_id:
                message_id = message.reply_to_message.message_id
                if message_id in user_message_mapping_law.keys():
                    user_id = user_message_mapping_law[message_id]
                    await bot.send_message(user_id, f'Відповідь:\n{message.text}')
                    await bot.send_message(chat_id=ADMIN_LAW_USER_ID, text='Відповідь була надіслана.')
                    await state.clear()
                else:
                    await message.answer('Користувача не знайдено.')
                    # print(message_id)
            else:
                await message.answer('Відповідайте на повідомлення користувача, щоб відправити відповідь.')

    if message.reply_markup is not None:
        await forward_to_law_admin(message)
        await state.clear()
    else:
        await state.set_state(Form.awaiting_question_law.state)

        async def check_for_question_law(message: Message):
            check_state = await state.get_state()
            if check_state == Form.awaiting_question_law.state:
                await forward_to_law_admin(message)

        @router.message()
        async def forward_message_law_handler(message: Message):
            await check_for_question_law(message)


# VPO
@router.message(F.text == 'ВПО')
@router.message(Command('VPO'))
async def process_VPO(message: Message, state: FSMContext):
    await message.answer('Виберіть опцію', reply_markup=VPO)
    await state.set_state(Form.vpo_state)


@router.message(F.text == 'Як отримати такий статус?')
@router.message(Command('get_VPO_status'))
async def get_status_vpo(message: Message, state: FSMContext):
    await message.answer(status_vpo_txt, parse_mode='HTML')
    await state.clear()


@router.message(F.text == "Права та обов'язки")
@router.message(Command('rights_and_duties'))
async def get_rights_vpo(message: Message, state: FSMContext):
    await message.answer(rights_vpo_txt, parse_mode='HTML', reply_markup=rights_and_duties_site)
    await state.clear()


# MILITARY
@router.message(F.text == 'Військовим')
@router.message(Command('for_military'))
async def process_military(message: Message, state: FSMContext):
    await message.answer('Виберіть опцію', reply_markup=military)
    await state.set_state(Form.military_state)


@router.message(F.text == 'Як отримати допомогу?')
@router.message(Command('help_for_military'))
async def get_help(message: Message, state: FSMContext):
    await message.answer(help_military_txt, parse_mode='HTML')
    await state.clear()


@router.message(F.text == 'Новий закон про мобілізацію')
@router.message(Command('mobilization_law'))
async def mobilization_military(message: Message, state: FSMContext):
    await message.answer(mobilization_military_txt, parse_mode='HTML')
    await state.clear()


# WAR VICTIMS
@router.message(F.text == 'Постраждалим від війни')
@router.message(Command('war_victims'))
async def process_war_victims(messsage: Message, state: FSMContext):
    await messsage.answer('Виберіть опцію', reply_markup=war_victims)
    await state.set_state(Form.war_victims_state)


@router.message(F.text == "Допомога")
@router.message(Command('help_for_war_victims'))
async def help_war_victims(message: Message, state: FSMContext):
    photos = [
        'images/table1.png',
        'images/table2.png',
        'images/table3.png'
    ]
    media_group = []
    for photo in photos:
        try:
            with open(photo, 'rb') as file:
                media_group.append(InputMediaPhoto(media=BufferedInputFile(file.read(), filename=os.path.basename(photo))))
        except Exception as error:
            print(f'{error}')
    await message.answer_media_group(media_group)
    await message.answer(war_victims_help_txt, parse_mode='HTML', reply_markup=war_victims_help_site)
    await state.clear()


@router.message(F.text == 'Діти')
@router.message(Command('war_victims_kids'))
async def help_war_victims(message: Message, state: FSMContext):
    await message.answer(war_victims_kids_txt, parse_mode='HTML')
    await state.clear()


@router.message(F.text == 'Майно')
@router.message(Command('war_victims_property'))
async def help_war_victims(message: Message, state: FSMContext):
    await message.answer(war_victims_property_txt, parse_mode='HTML', reply_markup=war_victims_property_info)
    await state.clear()


# VIOLENCE
@router.message(F.text == 'Насилля: що робити?')
@router.message(Command('violence'))
async def violence_help(message: Message, state: FSMContext):
    await message.answer(violence_txt, parse_mode='HTML')
    await state.clear()


# EVACUATION
@router.message(F.text == 'Порядок евакуації')
@router.message(Command('evacuation_plan'))
async def evacuation_plan(message: Message, state: FSMContext):
    await message.answer(evacuation_plan_txt, parse_mode='HTML')
    await state.clear()


# PSYCHOLOGICAL HELP
@router.message(F.text == 'Психологічна допомога')
@router.message(Command('psychological_help'))
async def psychological_help(message: Message, state: FSMContext):
    await message.answer(psychological_help_txt, parse_mode='HTML')
    await state.clear()


# BACK
@router.message(F.text == 'назад')
@router.message(Command('back'))
async def get_back(message: Message, state: FSMContext):
    await message.answer('Добре!', reply_markup=main)
    await state.clear()


# HELP WITH BOT
@router.message(Command('help'))
async def bot_help(message: Message, state: FSMContext):
    await message.answer(help_txt)
    await state.clear()