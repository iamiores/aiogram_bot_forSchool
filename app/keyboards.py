from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


'''
INLINE KEYBOARDS
'''
rights_and_duties_site = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сайт', url='https://kaplvested.info/konsultant/aktualno-pid-chas-voiennoho-stanu/prava-ta-oboviazky-vpo')]
])
war_victims_property_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посилання', url='https://youtu.be/eCkXhf6H_hY')]
])

war_victims_help_site = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сайт', url='https://naiu.org.ua/dovidnyky-dopomoga-postrazhdalym-vnaslidok-vijny-vid-derzhavy/')]
])


'''
REPLY KEYBOARDS
'''
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ВПО'), KeyboardButton(text='Військовим')],
    [KeyboardButton(text='Постраждалим від війни')],
    [KeyboardButton(text='Насилля: що робити?'), KeyboardButton(text='Порядок евакуації')],
    [KeyboardButton(text='Психологічна допомога')],
    [KeyboardButton(text="Зворотній зв'язок")]],

    resize_keyboard=True)

VPO = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Як отримати такий статус?')],
    [KeyboardButton(text="Права та обов'язки")],
    [KeyboardButton(text='назад')]],

    resize_keyboard=True, input_field_placeholder='ВПО')

military = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Як отримати допомогу?')],
    [KeyboardButton(text='Новий закон про мобілізацію')],
    [KeyboardButton(text='назад')]],

    resize_keyboard=True, input_field_placeholder='Військовим')

war_victims = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Допомога')],
    [KeyboardButton(text='Діти'), KeyboardButton(text='Майно')],
    [KeyboardButton(text='назад')]],

    resize_keyboard=True, input_field_placeholder='Постраждалим від війни')

support = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Потрібне уточнення'), KeyboardButton(text='Технічна підтримка')],
    [KeyboardButton(text='назад')]],

    resize_keyboard=True, input_field_placeholder="Зворотній зв'язок")
