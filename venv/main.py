""" Altair8 HUB Interface telegram bot ver 0.1.5
"""

# Import
from pymongo import MongoClient

import logging

from telegram import Bot
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext

TG_TOKEN = " "
MONGODB_LINK = " "
MONGO_DB = "HUB"

# -------------------------------
# Bot Logic
# -------------------------------
# Connect to DataBase
mondb = MongoClient(MONGODB_LINK)[MONGO_DB]

# Login Keyboard
contact_keyboard = KeyboardButton('Войти', request_contact=True)
custom_keyboard_login = [[contact_keyboard]]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(custom_keyboard_login, resize_keyboard=True)

CALLBACK_MM = "cb_mm"
CALLBACK_MM_HUB = "cb_mm_hs"
CALLBACK_MM_CHATS = "cb_mm_ch"
CALLBACK_MM_SCHLED = "cb_mm_sch"
CALLBACK_MM_TASKS = "cb_mm_ts"
CALLBACK_MM_TODO = "cb_mm_todo"
CALLBACK_MM_MUSIC = "cb_mm_mus"
CALLBACK_MM_SETTING = "cb_mm_setng"

CALLBACK_SM_ADDH = "cb_sm_add_new_hub"
CALLBACK_SM_RMH = "cb_sm_remove_my_hub"
CALLBACK_SM_NOTIFICATION = "cb_sm_notification"

CALLBACK_ADDHM_DEV = "cb_1add_hub_menu_1"
CALLBACK_ADDHM_HARD = "cb_1add_hub_menu_2"
CALLBACK_ADDHM_SOC = "cb_1add_hub_menu_3"
CALLBACK_ADDHM_ART = "cb_1add_hub_menu_4"
CALLBACK_ADDHM_GEEK = "cb_1add_hub_menu_5"

CALLBACK_RMHM_DEV = "cb_0rm_hub_menu_1"
CALLBACK_RMHM_HARD = "cb_0rm_hub_menu_2"
CALLBACK_RMHM_SOC = "cb_0rm_hub_menu_3"
CALLBACK_RMHM_ART = "cb_0rm_hub_menu_4"
CALLBACK_RMHM_GEEK = "cb_0rm_hub_menu_5"

CALLBACK_RR = "cb_rr"


def get_hubs(bool_list):
    keyboard = []
    if int(bool_list[1]):
        keyboard.append([InlineKeyboardButton("🖥    DEV.HUB", url="https://t.me/joinchat/OPPf1lTKYcszVxfih0m2jw")])
    if int(bool_list[5]):
        keyboard.append([InlineKeyboardButton("🎮   GEEK.HUB", url="https://t.me/joinchat/OPPf1lDF0qoKXq7Wnn71eA")])
    if int(bool_list[3]):
        keyboard.append([InlineKeyboardButton("🗣    SOC.HUB", url="https://t.me/joinchat/OPPf1laFJhzZ6Sx88P0YOQ")])
    if int(bool_list[4]):
        keyboard.append([InlineKeyboardButton("🔳    ART.HUB", url="https://t.me/joinchat/OPPf1leFxg4vdBbkler_Xg")])
    if int(bool_list[6]):
        keyboard.append([InlineKeyboardButton("🏴‍☠   DARK.HUB️", url="https://t.me/joinchat/OPPf1ldtdd0CxeejqWUDdg")])
    if int(bool_list[2]):
        keyboard.append([InlineKeyboardButton("🔌   HARD.HUB", url="https://t.me/joinchat/OPPf1lh2GTulebNiu34jEw")])

    keyboard.append([InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM)])
    return InlineKeyboardMarkup(keyboard)


def get_back_mm():
    keyboard = [[InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM)]]
    return InlineKeyboardMarkup(keyboard)


# Main Menu
def get_main_menu(user):
    keyboard = [
        [
            InlineKeyboardButton("🟩  [HUB] chanel", url="https://t.me/thehub_su"),
        ],
        [
            InlineKeyboardButton("🕸  My Small HUBs", callback_data=CALLBACK_MM_HUB),
        ],
        [
            InlineKeyboardButton("📆 Расписание", callback_data=CALLBACK_MM_SCHLED),
            InlineKeyboardButton("📋 Задачи", callback_data=CALLBACK_MM_TASKS),
        ],
        [
            InlineKeyboardButton("🌐  Мои Чаты", callback_data=CALLBACK_MM_CHATS),
            InlineKeyboardButton("📝  TO DO", callback_data=CALLBACK_MM_TODO),
        ],
        [
            InlineKeyboardButton("🎵  Музыка Дня", callback_data=CALLBACK_MM_MUSIC),
        ],
        [
            InlineKeyboardButton("ℹ️  Дополнительно️", callback_data=CALLBACK_MM_SETTING),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_settings(user):
    user_notify = "🔈 Уведомления включены" if user.get("user_notification") else "🔇 Уведомления отключены"
    keyboard = [
        [
            InlineKeyboardButton("➕  Добавить Хаб", callback_data=CALLBACK_SM_ADDH),
            InlineKeyboardButton("❌  Удалить Хаб", callback_data=CALLBACK_SM_RMH),
        ],
        [
            InlineKeyboardButton("{}".format(user_notify), callback_data=CALLBACK_SM_NOTIFICATION),
        ],
        [
            InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_add_hubs(bool_list):
    keyboard = []
    if int(bool_list[1]) == 0:
        keyboard.append([InlineKeyboardButton("🖥    DEV.HUB", callback_data=CALLBACK_ADDHM_DEV)])
    if int(bool_list[2]) == 0:
        keyboard.append([InlineKeyboardButton("🔌   HARD.HUB", callback_data=CALLBACK_ADDHM_HARD)])
    if int(bool_list[3]) == 0:
        keyboard.append([InlineKeyboardButton("🗣    SOC.HUB", callback_data=CALLBACK_ADDHM_SOC)])
    if int(bool_list[4]) == 0:
        keyboard.append([InlineKeyboardButton("🔳    ART.HUB", callback_data=CALLBACK_ADDHM_ART)])
    if int(bool_list[5]) == 0:
        keyboard.append([InlineKeyboardButton("🎮   GEEK.HUB", callback_data=CALLBACK_ADDHM_GEEK)])

    keyboard.append([InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM_SETTING)])
    return InlineKeyboardMarkup(keyboard)


def get_remove_hubs(bool_list):
    keyboard = []
    if int(bool_list[1]):
        keyboard.append([InlineKeyboardButton("🖥    DEV.HUB", callback_data=CALLBACK_RMHM_DEV)])
    if int(bool_list[2]):
        keyboard.append([InlineKeyboardButton("🔌   HARD.HUB", callback_data=CALLBACK_RMHM_HARD)])
    if int(bool_list[3]):
        keyboard.append([InlineKeyboardButton("🗣    SOC.HUB", callback_data=CALLBACK_RMHM_SOC)])
    if int(bool_list[4]):
        keyboard.append([InlineKeyboardButton("🔳    ART.HUB", callback_data=CALLBACK_RMHM_ART)])
    if int(bool_list[5]):
        keyboard.append([InlineKeyboardButton("🎮   GEEK.HUB", callback_data=CALLBACK_RMHM_GEEK)])

    keyboard.append([InlineKeyboardButton("⬅️     Назад️", callback_data=CALLBACK_MM_SETTING)])
    return InlineKeyboardMarkup(keyboard)


def get_rereg_button():
    keyboard = [
        [
            InlineKeyboardButton("📲  Сменить номер", callback_data=CALLBACK_RR),
        ],
        [
            InlineKeyboardButton("Служба поддержки", url="https://t.me/HUBsup"),
        ],
        [
            InlineKeyboardButton("🔥 Наш сайт! ", url="https://www.thehub.su")
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def on_start(update: Update, context: CallbackContext):
    message = update.message
    user = mondb.users.find_one({"user_id": message.chat.id})
    logging.info(message.chat.id)
    if not user:
        message.reply_text(
            'Привет! Для того что бы войти в систему необходиму залогиниться!',
            reply_markup=REPLY_KEYBOARD_MARKUP
        )
    else:
        message.reply_text(
            "Основное меню: ",
            reply_markup=get_main_menu()
        )


# IF user message == contact
def on_contact(update: Update, context: CallbackContext):
    message = update.message
    user_phone_number = 0
    user_chat_id = 0
    # IF user get another Contact
    if message.chat_id == int(message.contact['user_id']):
        if message.contact:
            num1 = str(message.contact['phone_number'])
            user_phone_number = 0

            for i in range(-10, 0):
                user_phone_number += int(num1[i]) * (10 ** ((i + 1) * -1))
            user_chat_id += int(message.contact['user_id'])

        user = login_user(mondb, user_chat_id, user_phone_number)
        logging.info(user)
        if not user:

            mondb.ValentineEvent_users.insert(
                {user_id: user_chat_id,
                  user_phone: user_phone_number, }
            )


            """message.reply_text(
                'Ошибка! Указанный пользователь не найден.',
                reply_markup=ReplyKeyboardRemove()
            )
            message.reply_text(
                'Возможный проблемы: \
                \n1. Если в Анкете вы указали некорректный номер можете сменить его нажав кнопку ниже. \
                \n2. Если вы заполнили анкету более чем 1 неделю назад, пожалуйста обратитесь к службе поддержки.\
                \n3. Если вы еще не заполняли анкету, самое время сделать это перейдя на наш сайт!',
                reply_markup=get_rereg_button()
            )
            """
        else:
            message.reply_text(
                'Вы успешно авторизированы!',
                reply_markup=ReplyKeyboardRemove()
            )
            message.reply_text(
                'Вас приветсвует Altair8 - интерфейс взаимодействия с H.U.B. ver 0.1. Интересного вам времяпрепровождения!\
                 \nОсновное меню:',
                reply_markup=get_main_menu()
            )
    else:
        message.reply_text(
            'Ошибка доступа! Указанный номер не соответсвует UserID.',
            reply_markup=ReplyKeyboardRemove()
        )


# User Register
def login_user(mondb, user_id, user_phone_number):
    user = mondb.users.find_one({"user_phone": user_phone_number})
    logging.info("user_phone: " + str(user_phone_number))
    if user != None and user.get('user_id') is None:
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'user_id': user_id}}
        )
        return user
    else:
        return None


# Command to edit phone number from DB
def do_changephone(update: Update, context: CallbackContext):
    # IF incorrect command input
    try:
        # Parcing user input
        old_phone_number = int(update.message.text[13:23])
        user_new_phone_number = int(update.message.text[26:36])
        user_name = update.message.text[37:]
        user = mondb.users.find_one({"user_phone": old_phone_number})
    except:
        user = None
        user_name = ''
        user_new_phone_number = 0

    if not user:
        update.message.reply_text(
            'Ошибка! Указаный номер не найден!',
        )
    elif user.get('user_id') is None and user.get("user_name") == user_name:
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'user_phone': user_new_phone_number,
                      'user_id': update.message.chat_id
                      }}
        )
        update.message.reply_text(
            'Номер успешно изменен! Перезапустите бота /start',
        )
    else:
        update.message.reply_text(
            'Ошибка! Не соответсвие данных!',
        )


def do_sendmessage(update: Update, context: CallbackContext):
    lead_message = update.message.text
    user = mondb.users.find_one({"user_id": update.message.chat_id})
    user_lead = int(user.get("user_hubs") / 1000000)
    if user_lead == 1:
        update.message.reply_text(
            'Только Лид может отправлять общую задачу!',
        )
    else:
        # Slot choice
        # TODO inline mode
        if len(lead_message) > 11:
            if lead_message[10] == '0':
                for x in mondb.users.find({"lead": True}):
                    if not (x.get("user_id") is None):
                        if str(x.get("user_hubs"))[0] == lead_message[12]:
                            context.bot.send_message(
                                chat_id=x.get("user_id"),
                                text=lead_message[11:],
                            )
            if lead_message[10] == '1':
                for x in mondb.users.find({"lead": True}):
                    if not (x.get("user_id") is None):
                        context.bot.send_message(
                            chat_id=x.get("user_id"),
                            text=lead_message[11:],
                        )
            if lead_message[10] == '2':
                for x in mondb.users.find():
                    if not (x.get("user_id") is None):
                        if str(x.get("user_hubs"))[user_lead - 1] == '1':
                            context.bot.send_message(
                                chat_id=x.get("user_id"),
                                text=lead_message[11:],
                            )
            if lead_message[10] == '3':
                for x in mondb.users.find():
                    if not (x.get("user_id") is None):
                        context.bot.send_message(
                            chat_id=x.get("user_id"),
                            text=lead_message[11:],
                        )
            else:
                update.message.reply_text(
                    'Неверно указан ключ отправления!',
                )
        else:
            update.message.reply_text(
                'Слишком короткое сообщение!',
            )


# Sticker Time! Dont Touch!
#
def handle_docs_audio(update: Update, context: CallbackContext):
#     # Получим ID Стикера
     sticker_id = update.message.sticker.file_id
     chatid = update.effective_message.chat_id
     context.bot.send_message(
        chat_id=chatid,
        text="Sticker ID " + sticker_id,
     )



# Command to event new day to small HUB Schledule

def do_addevent(update: Update, context: CallbackContext):
    text = update.message.text
    user = mondb.users.find_one({"user_id": update.message.chat_id})
    user_lead = int(user.get("user_hubs") / 1000000)
    if user_lead == 1:
        update.message.reply_text(
            'Только Лид может изменять расписание!',
        )
    else:
        # Slot choice
        # TODO Edit this command, automatic slot choice
        if text[10] == '1':
            mondb.allschledule.update_one(
                {'hub_id': user_lead - 1},
                {'$set': {'event1': text[12:]}}
            )
        if text[10] == '2':
            mondb.allschledule.update_one(
                {'hub_id': user_lead - 1},
                {'$set': {'event2': text[12:]}}
            )
        if text[10] == '3':
            mondb.allschledule.update_one(
                {'hub_id': user_lead - 1},
                {'$set': {'event3': text[12:]}}
            )


# Telegram inline menu buttons handler
def keyboard_call_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user = mondb.users.find_one({"user_id": update.effective_message.chat_id})

    if data == CALLBACK_MM:
        query.edit_message_text(
            text="Основное меню: ",
            reply_markup=get_main_menu()
        )
    elif data == CALLBACK_MM_HUB:
        query.edit_message_text(
            text="Ваши активные Хабы: ",
            reply_markup=get_hubs(str(user.get("user_hubs")))
        )
        # TODO Inline music add
    elif data == CALLBACK_MM_MUSIC:
        chatid = update.effective_message.chat_id
        query.edit_message_text(
            text="Музыка дня, для души и работы от участников Хаба. Сегодня в честь запуска музыка от @MON0makh\
         \nЗаказать плейлист можно у @MON0makh 🎧",
        )
        # TODO Local audio need
        context.bot.send_sticker(chatid, 'CAACAgEAAxkBAAIDMV92U2Sk4DVLErXtBFPWgQhfmqh1AAJhAAPArAgjT8wG8ZJFRc0bBA')
        for i in range(1, 7):
            context.bot.send_audio(
                chat_id=chatid,
                audio='https://raw.githubusercontent.com/POSE1D0N-AP/Altair8tb/master/music%20of%20day/{}.mp3'.format(
                    i),
            )
        context.bot.send_message(
            chat_id=chatid,
            text="Основное меню",
            reply_markup=get_main_menu(),
        )
    elif data == CALLBACK_MM_SCHLED:
        chatid = update.effective_message.chat_id
        # TODO add BIGHUB Schledule
        for i in range(1, 7):
            if str(user.get("user_hubs"))[i]:
                table = mondb.allschledule.find_one({"hub_id": i})
                if table != None:
                    text = table.get('hub_name') + ": "
                    if table.get('event1') != None:
                        text += "\n" + table.get('event1')
                    if table.get('event2') != None:
                        text += "\n" + table.get('event2')
                    if table.get('event3') != None:
                        text += "\n" + table.get('event3')

                    # IF schledule empty
                    if len(text) > 10:
                        context.bot.send_message(
                            chat_id=chatid,
                            text="{}".format(text),
                        )
                    else:
                        context.bot.send_message(
                            chat_id=chatid,
                            text="{}".format(text + "Пока ничего..."),
                        )

    elif data == CALLBACK_MM_SETTING:
        query.edit_message_text(
            text="Дополнительное меню",
            reply_markup=get_settings(user)
        )
    elif data == CALLBACK_MM_TASKS:
        query.edit_message_text(
            text="Altair8 все еще находится в разработке, на данный момент эта функция не доступна, но скоро мы это испраим.\
            \nНадеемся на ваше понимание! Если вы обнаружили какие либо баги в работе системы Altair8, пожалуйста сообщите нам: @HUBsup",
            reply_markup=get_back_mm()
        )
    elif data == CALLBACK_MM_TODO:
        query.edit_message_text(
            text="Altair8 все еще находится в разработке, на данный момент эта функция не доступна, но скоро мы это испраим.\
            \nНадеемся на ваше понимание! Если вы обнаружили какие либо баги в работе системы Altair8, пожалуйста сообщите нам: @HUBsup",
            reply_markup=get_back_mm()
        )
    elif data == CALLBACK_MM_CHATS:
        query.edit_message_text(
            text="Altair8 все еще находится в разработке, на данный момент эта функция не доступна, но скоро мы это испраим.\
            \nНадеемся на ваше понимание! Если вы обнаружили какие либо баги в работе системы Altair8, пожалуйста сообщите нам: @HUBsup",
            reply_markup=get_back_mm()
        )
    elif data == CALLBACK_RR:
        query.edit_message_text(
            text="Если вы ввели некорректный номер телефона в анкете, вы можете сменить номер следующей командой:\
            \nВведите /editphone <старый номер телефона> <новый номер телефона> <имя-фамилию как в анкете>. Пример:\
            \n/editphone +7XXXXXXXXXX +7YYYYYYYYYY Владимир Мономах\
            \nРаботает только для не авторизованных пользователей! Номер важно вводить без пробелов с одну строку."
        )
    elif data == CALLBACK_SM_ADDH:
        query.edit_message_text(
            text="Здесь вы можете войти в новые Хабы.\
            \nПосле добавления новый Хаб появится в списке в Основном Меню",
            reply_markup=get_add_hubs(str(user.get("user_hubs")))
        )
    elif data == CALLBACK_SM_RMH:
        query.edit_message_text(
            text="Здесь вы можете удалить свои Хабы.\
            \nПосле удаления Хаб исчезнет из списка в Основном Меню. Вы можете восстановить его в любой момент.",
            reply_markup=get_remove_hubs(str(user.get("user_hubs")))
        )
    elif data == CALLBACK_ADDHM_DEV or data == CALLBACK_ADDHM_HARD or \
            data == CALLBACK_ADDHM_SOC or data == CALLBACK_ADDHM_ART or \
            data == CALLBACK_ADDHM_GEEK or data == CALLBACK_RMHM_DEV or \
            data == CALLBACK_RMHM_HARD or data == CALLBACK_RMHM_SOC or \
            data == CALLBACK_RMHM_ART or data == CALLBACK_RMHM_GEEK:
        logging.warning(data)
        user_hubs = str(user.get("user_hubs"))
        user_now_edit_hub = int(data[-1])
        user_hubs = user_hubs[0:user_now_edit_hub] + data[3] + user_hubs[(user_now_edit_hub + 1):]
        user["user_hubs"] = user_hubs
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'user_hubs': int(user_hubs)}}
        )

        if int(data[3]) == 0:
            query.edit_message_text(
                text="Здесь вы можете удалить свои Хабы.\
                        \nПосле удаления Хаб исчезнет из списка в Основном Меню. Вы можете восстановить его в любой момент.",
                reply_markup=get_remove_hubs(str(user.get("user_hubs")))
            )
        else:
            query.edit_message_text(
                text="Здесь вы можете войти в новые Хабы.\
                               \nПосле добавления новый Хаб появится в списке в Основном Меню",
                reply_markup=get_add_hubs(str(user.get("user_hubs")))
            )
    elif data == CALLBACK_SM_NOTIFICATION:
        mondb.users.update_one(
            {'_id': user['_id']},
            {'$set': {'user_notification': not user['user_notification']}}
        )
        user['user_notification'] = not user['user_notification']

        query.edit_message_text(
            text="Дополнительное меню",
            reply_markup=get_settings(user)
        )


def main():
    updater = Updater(
        token=TG_TOKEN,
        use_context=True,
    )

    logging.info("Altair8 started")
    # Commands handler add, IF you u need add new command use it
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(CommandHandler('editphone', do_changephone))
    dp.add_handler(CommandHandler('addevent', do_addevent))
    dp.add_handler(CommandHandler('sendtask', do_sendmessage))
    dp.add_handler(MessageHandler(Filters.sticker, handle_docs_audio))

    dp.add_handler(CallbackQueryHandler(callback=keyboard_call_handler, pass_chat_data=True))
    dp.add_handler(MessageHandler(Filters.contact, on_contact))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
