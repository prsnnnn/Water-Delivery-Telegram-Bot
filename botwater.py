# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from telebot import types
import re
import time
from telebot.apihelper import ApiTelegramException
from water_classes import usrs, bans, orders, comp, logs, AdminService, PricingService, PhoneNumber, OrderService
from keybords import Keyboards
import admin_handles
from logger_setup import setup_logging
from bot_instance import bot
logger = setup_logging(mongo_collection=logs)

@bot.message_handler(commands=["start"])
def start_command(message):
    if usrs.find_one({'tgid': message.chat.id}):
        bot.send_message(message.chat.id, f'ℹ* Головне меню*', parse_mode='Markdown',
                         reply_markup=Keyboards.main_menu())
    else:
        bot.send_message(message.chat.id,
                         f'*📍 Вас вітає доставка води «Aqua Way» - надійна та якісна вода для вашого дому та офісу*\n\nОберіть пункт меню:',
                         parse_mode='Markdown', reply_markup=Keyboards.main_menu())
        usrs.insert_one({'tgid': message.chat.id, 'name': None, 'num': None, 'adress': None, 'ord': 0})
        logger.info('User %s was recorded in DB', message.chat.id)

@bot.message_handler(content_types=['text'])
def start_command_handler(message):
    def mu(message):
        bot.send_message(message.chat.id, f'ℹ* Головне меню*', parse_mode='Markdown', reply_markup=Keyboards.main_menu())
    def deliver2(message, ordlist):
        date = message.text
        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if date != '↩ Головне меню':
            if re.match(pattern, date):
                ordlist['date'] = date
                bot.send_message(message.chat.id,'🛍')
                bot.send_message(message.chat.id,
                                     f"*📍 Замовлення 📍*\n\nІм'я: *{ordlist['name']}*\nТелефон:\n*{ordlist['num']}*\nАдреса:\n*{ordlist['adress']}*\nК-сть пляшок: *{ordlist['val']}шт*.\nДата: *{ordlist['date']}*\n\n💰Ціна замовлення: *{ordlist['price']}*\n\n*Очікуйте на дзвінок оператора☺*",
                                     parse_mode='Markdown')
                name = bot.get_chat_member(message.chat.id, message.chat.id).user.username
                for m in AdminService.all_ids():
                    try:
                        bot.send_message(m, f'<b>+1 ЗАМОВЛЕННЯ\nTgID: <code>{message.chat.id}</code>\nUsername: @{name}</b>\n\n/admin', parse_mode='HTML')
                    except ApiTelegramException as e:
                        if e.error_code==403:
                            logger.info("Admin %s has blocked the bot", m)
                orders.insert_one(ordlist)
                mu(message)
            else:
                k = bot.send_message(message.chat.id,
                                     f'*Невірний формат ❌*\n\n*Введіть дату доставки в форматі* `xx.xx.xxxx`',
                                     parse_mode='Markdown')
                bot.register_next_step_handler(k, deliver2, ordlist)
        else:
            mu(message)

    def deliver1(message):
        user = usrs.find_one({'tgid': message.chat.id})
        try:
            val = int(message.text)
        except ValueError:
            val = 0
        name = user['name']
        number=PhoneNumber.get_num(message.chat.id)
        adress = user['adress']
        if val == 0:
            mu(message)
        elif val > 30:
            bot.send_message(message.chat.id, f'Максимальна кількість пляшок для замовлення - *30* ❌',
                             parse_mode='Markdown')
            mu(message)
        elif val < 0:
            bot.send_message(message.chat.id, f'Невірний формат ❌')
            mu(message)
        else:
            price = PricingService.calculate(val)
            ordlist = {'tgid': message.chat.id, 'type': None, 'name': name, 'num': number,
                       'adress': adress, 'val': val, 'price': price}
            k2 = bot.send_message(message.chat.id, f'*Введіть дату доставки в форматі* `xx.xx.xxxx`',
                                  parse_mode='Markdown', reply_markup=Keyboards.back_to_main_menu())
            bot.register_next_step_handler(k2, deliver2, ordlist)

    def deliverr(message):
        if message.text == '💧 Замовити доставку води':
            k = bot.send_message(message.chat.id, f'Введіть кількість води в пляшках *19л:*', reply_markup=Keyboards.back_to_main_menu(),
                                 parse_mode='Markdown')
            bot.register_next_step_handler(k, deliver1)
        elif message.text == '🛒 Перейти в магазин':
            mu(message)
            bot.send_message(message.chat.id, f'🛒 Оберіть категорію товарів:', reply_markup=Keyboards.inline_shop_catalog())
        else:
            mu(message)
    banned_user = bans.find_one({'tgid': message.chat.id}, {'_id': 1})
    isban = banned_user is None
    if isban:
        user = usrs.find_one({'tgid': message.chat.id})
        if message.text == '💧 Замовити':
            txt = ''
            if user['name'] is None:
                txt += "- Ім'я 👤\n"
            if user['num'] is None:
                txt += "- Номер телефону 📱\n"
            if user['adress'] is None:
                txt += "- Адреса 🏠\n"
            if txt == '':
                order = orders.find_one({'tgid': message.chat.id,'type': None}, {'_id': 1})
                ordfind = order is not None
                if not ordfind:
                    bot.send_message(message.chat.id,'🛒')
                    k = bot.send_message(message.chat.id, f'*Оберіть пункт меню:*', parse_mode='Markdown',
                                         reply_markup=Keyboards.order_inline())
                    bot.register_next_step_handler(k, deliverr)
                else:
                    bot.send_message(message.chat.id,
                                     f'*💫 Ви вже зробили замовлення. Очікуйте на підтвердження оператора*',
                                     parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id,
                                 f'❌ *Немає наступної інформації:\n{txt}\nДоповніть її в "🔑 Мій кабінет"*',
                                 parse_mode='Markdown')
        elif message.text == '🔑 Мій кабінет':
            num=None
            if user['num'] is not None:
                num=PhoneNumber.phnum(PhoneNumber.get_num(message.chat.id))
            bot.send_message(message.chat.id,'🔐')
            bot.send_message(message.chat.id,
                             f"*🔑 Ваш кабінет*\n\n👤 Ім'я: *{user['name']}*\n📱 Телефон:\n*{num}*\n🏠 Адреса:\n*{user['adress']}*\n🚐 Успішних замовлень: *{user['ord']}*",
                             parse_mode='Markdown', reply_markup=Keyboards.personal_cabinet())
        elif message.text == '☎️ Контакти':
            site = 'https://aqua-way.dp.ua/'
            link = f'<a href="{site}">AquaWay</a>'
            bot.send_message(message.chat.id,'📞')
            bot.send_message(message.chat.id,
                             f'<b>ℹ Наші контакти</b>\n\n<b>🌐 Вебсайт:</b> <b>{link}</b>\n<b>📷 Instagram: </b><code>@aqua_way.dp</code>\n<b>☎ Телефони для замовлення:</b>\n<code>+38(063)-135-91-56</code>\n<code>+38(066)-004-59-99</code>\n<code>+38(098)-998-07-37</code>\n<b>🏠 Адреса компанії:</b>\n<code>м. Дніпро, вул. Центральна, 56, офіс 30</code>\n<b>🕒 Графік роботи контакт центру:</b>\n<code>8:00 – 18:00</code>',
                             parse_mode='HTML', disable_web_page_preview=True)
        elif message.text == '💰 Ціни':
            bot.send_message(message.chat.id,'💰')
            bot.send_message(message.chat.id,
                             '🚚 *Доставка води\n\nПрайс:\n\n1шт - 150₴/19л\n2шт - 125₴/19л\n3-4шт - 120₴/19л\n5-14шт - 110₴/19л\n15+шт - договірна*',
                             parse_mode='Markdown')
        elif message.text == '📌 Інформація':
            bot.send_message(message.chat.id,
                             f'*«AQUA WAY» — ми те, що ми вживаємо*\n\n*💧 «AQUA WAY»* – це унікальна структурована вода , яка за допомогою мінералізації, технології очищення та пом’якшення, забезпечує життєдіяльність людини енергією, впливає на працездатність, зберігає тонус на протязі всього дня.\n\n*♻ «AQUA WAY»* відповідає всім сучасним вимогам та нормам екології, не має обмежень по віку та діяльності людини.\n\n🚀 *Наші переваги:*\n- Гарантуємо своєчасну та безкоштовну доставку у будь-яку частину міста\n- Індивідуальні знижки та комплексний підхід до кожного клієнта\n- Зручний спосіб оплати та надання документів для звіту',
                             parse_mode='Markdown')
        elif message.text == '🌍 Перейти на сайт':
            bot.send_message(message.chat.id,'💻')
            bot.send_message(message.chat.id,
                             '<b>🌍 Замовити доставку можна також через наш вебсайт:\n https://aqua-way.dp.ua/</b>',
                             parse_mode='HTML', reply_markup=Keyboards.website_inline(), disable_web_page_preview=True)
        elif message.text == '🖼 Перейти в інстаграм':
            bot.send_message(message.chat.id,'✨')
            bot.send_message(message.chat.id, '<b>🖼   Наш інстаграм:\n https://www.instagram.com/aqua_way.dp</b>',
                             parse_mode='HTML', reply_markup=Keyboards.insta_inline())
        elif message.text == "↩ Головне меню":
            mu(message)
        else:
            bot.send_message(message.chat.id, f'*Не розумію Вас\nОберіть пункт меню нижче:*', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f'Ви були заблоковані 🚫')


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    def mu(call):
        bot.send_message(call.from_user.id, f'ℹ* Головне меню*', parse_mode='Markdown', reply_markup=Keyboards.main_menu())
    if call.data == 'mu':
        mu(call)
    elif call.data == 'cab':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        user = usrs.find_one({'tgid': call.from_user.id})
        def nxt3(message):
            if message.text != '↩ Головне меню':
                usrs.update_one({'tgid': message.from_user.id}, {"$set": {'adress': message.text}})
                bot.send_message(call.from_user.id, f"*Інформацію заповнено ✅*", parse_mode='Markdown')
            mu(message)
        def nxt2(message):
            if message.text == '↩ Головне меню':
                mu(message)
            else:
                phone = message.text
                if phone.isdigit() and len(phone) == 10 and phone.startswith('0'):
                    usrs.update_one({'tgid': message.from_user.id}, {"$set": {'num': phone}})
                    muadr = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    if user['adress'] is not None:
                        muadr.add(user['adress'])
                    muadr.add('↩ Головне меню')
                    k = bot.send_message(call.from_user.id, "Введіть Вашу домашню адресу:", reply_markup=muadr,
                                         parse_mode='Markdown')
                    bot.register_next_step_handler(k, nxt3)
                else:
                    munum = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    if user['num'] is not None:
                        munum.add(user['num'])
                    munum.add('↩ Головне меню')
                    k = bot.send_message(call.from_user.id,
                                         "❌ Невірний формат\n\nВведіть Ваш номер телефону в форматі `0991113355`",
                                         reply_markup=munum, parse_mode='Markdown')
                    bot.register_next_step_handler(k, nxt2)
        def nxt1(message):
            if message.text == '↩ Головне меню':
                mu(message)
            else:
                usrs.update_one({'tgid': message.from_user.id}, {"$set": {'name': message.text}})
                munum = types.ReplyKeyboardMarkup(resize_keyboard=True)
                if user['num'] is not None:
                    munum.add(user['num'])
                munum.add('↩ Головне меню')
                k = bot.send_message(call.from_user.id, f"Введіть Ваш номер телефону в форматі `0991113355`",
                                     reply_markup=munum, parse_mode='Markdown')
                bot.register_next_step_handler(k, nxt2)

        muname = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if user['name'] is not None:
            muname.add(user['name'])
        muname.add('↩ Головне меню')
        k = bot.send_message(call.from_user.id, f"Введіть Ваше ім'я", reply_markup=muname)
        bot.register_next_step_handler(k, nxt1)
    elif call.data == 'history':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        txt = '*Історія замовлень📋*\n\n'
        count = 0
        req1 = list(
            orders.find(
                {'tgid': call.from_user.id, 'type': None},
                {'val': 1, 'price': 1, 'date': 1}
            ).sort('_id', -1).limit(3)
        )
        for l in req1:
            count += 1
            txt += f'*{count}.*\nДата: *{l["date"]}*\nПляшок: *{l["val"]}шт*\nСума: *{l["price"]}*\nСтатус: *Обробка* 🕒\n'

        if count < 3:
            req2 = list(
                comp.find(
                    {'tgid': call.from_user.id, 'type': None},
                    {'val': 1, 'price': 1, 'date': 1}
                ).sort('_id', -1).limit(3 - count)
            )
            for k in req2:
                count += 1
                txt += f'*{count}.*\nДата: *{k["date"]}*\nПляшок: *{k["val"]}шт*\nСума: *{k["price"]}*\nСтатус: *Виконано* ✅\n'
        if count > 0:
            bot.send_message(call.from_user.id, txt, parse_mode='Markdown')
        else:
            bot.send_message(call.from_user.id, 'Ви ще не робили замовлень 😕', parse_mode='Markdown')
    elif call.data == 'i1':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        bot.send_message(call.from_user.id, f'🛒 Оберіть підходящу Вам механічну помпу:', reply_markup=Keyboards.inline_shop_s1())
    elif call.data == 'i2':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        bot.send_message(call.from_user.id, f'🛒 Оберіть підходящу Вам електричну помпу:', reply_markup=Keyboards.inline_shop_s2())
    elif call.data == 'i3':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        bot.send_message(call.from_user.id, f'🛒 Оберіть підходящу Вам ручку:', reply_markup=Keyboards.inline_shop_s3())
    elif call.data == 'i4':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        bot.send_message(call.from_user.id, f'🛒 Оберіть підходящу Вам підставку:', reply_markup=Keyboards.inline_shop_s4())
    elif call.data == 'shop':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        bot.send_message(call.from_user.id, f'🛒 Оберіть категорію товарів:', reply_markup=Keyboards.inline_shop_catalog())
    elif call.data == 'balon':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        inline_shop = types.InlineKeyboardMarkup()
        inline_b1 = types.InlineKeyboardButton('💲 Замовити', callback_data='balonbuy')
        inline_b2 = types.InlineKeyboardButton('↩️ Назад', callback_data='shop')
        inline_shop.add(inline_b1)
        inline_shop.add(inline_b2)
        img = open('../balon.jpg', 'rb')
        bot.send_photo(call.from_user.id, img, '*Балон 19л*\n\nЦіна: 350грн', reply_markup=inline_shop,
                       parse_mode='Markdown')
    elif call.data == 'pompa1':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        img = open('../pompa1.jpg', 'rb')
        bot.send_photo(call.from_user.id, img, '*Механічна помпа*\n\nЦіна: 150грн', reply_markup=Keyboards.inline_shop_pompa(call.data),
                       parse_mode='Markdown')
    elif call.data == 'pompa2':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        img = open('../pompa2.jpg', 'rb')
        bot.send_photo(call.from_user.id, img, '*Електрична помпа*\n\nЦіна: 350грн', reply_markup=Keyboards.inline_shop_pompa(call.data),
                       parse_mode='Markdown')
    elif call.data == 'shopback':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        inline_shop = types.InlineKeyboardMarkup()
        inline_b1 = types.InlineKeyboardButton('Балон', callback_data='balon')
        inline_b2 = types.InlineKeyboardButton('Механічна помпа', callback_data='pompa1')
        inline_b3 = types.InlineKeyboardButton('Електро помпа', callback_data='pompa2')
        inline_shop.add(inline_b1)
        inline_shop.add(inline_b2, inline_b3)
        bot.send_message(call.from_user.id, f'Оберіть товар, що Вас зацікавив:', reply_markup=inline_shop)
    elif call.data == 'balonbuy':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        OrderService.create(bot, call.from_user.id, 'balon', 350)
        bot.send_message(call.from_user.id, f'*🚐 Замовлення прийнято\nОчікуйте на дзвінок оператора☺*',
                         parse_mode='Markdown')
        mu(call)
    elif call.data == 'pompa1buy':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        OrderService.create(bot, call.from_user.id, 'pompa1', 150)
        bot.send_message(call.from_user.id, f'*🚐 Замовлення прийнято\nОчікуйте на дзвінок оператора☺*',
                         parse_mode='Markdown')
        mu(call)
    elif call.data == 'pompa2buy':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        OrderService.create(bot, call.from_user.id, 'pompa2', 350)
        bot.send_message(call.from_user.id, f'*🚐 Замовлення прийнято\nОчікуйте на дзвінок оператора☺*',
                         parse_mode='Markdown')
        mu(call)
    call3 = str(call.data)[:3]
    call4 = str(call.data)[:4]
    if call4 == 'item':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        result = int(call.data[4:])
        water=PricingService.return_catalog()
        inline_shop = types.InlineKeyboardMarkup()
        inline_b1 = types.InlineKeyboardButton('💲 Замовити', callback_data=f'ibuy{result}')
        inline_b2 = types.InlineKeyboardButton('↩️ Назад', callback_data='shop')
        inline_shop.add(inline_b1)
        inline_shop.add(inline_b2)
        bot.send_message(call.from_user.id,
                         f'<b>🔻 Товар: {water[result]["d"]}</b>\n\n💰 Ціна: <b>{water[result]["price"]}грн</b>\n\n<b><i>Підтвердити замовлення?</i></b>',
                         reply_markup=inline_shop, parse_mode='HTML')
    elif call4 == 'ibuy':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except ApiTelegramException:
            pass
        result = int(call.data[4:])
        water = PricingService.return_catalog()
        OrderService.create(bot, call.from_user.id, None, water[result]['price'], product_name=water[result]['d'])
        bot.send_message(call.from_user.id, f'*🚐 Замовлення прийнято\nОчікуйте на дзвінок оператора☺*',
                         parse_mode='Markdown')
        mu(call)
    result = call.data[3:]
    if call3 == 'ban':
        tr = bans.find_one({'tgid': int(result)}, {'_id': 1}) is not None
        if tr:
            bot.send_message(call.from_user.id, 'Користувач вже в бані')
        else:
            bans.insert_one({'tgid': int(result)})
            bot.send_message(call.from_user.id, f'Користувача `{result}` заблоковано ✅', parse_mode='Markdown')
    elif call3 == 'unb':
        tr = bans.find_one({'tgid': int(result)}, {'_id': 1}) is None
        if tr:
            bot.send_message(call.from_user.id, 'Користувач не знаходиться в бані')
        else:
            bans.delete_one({'tgid': int(result)})
            bot.send_message(call.from_user.id, f'Користувача `{result}` розблоковано ✅', parse_mode='Markdown')

import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()
if __name__ == '__main__':
    while True:
        try:
            logger.info('Starting bot %s',datetime.now(timezone.utc))
            print('Telegram Bot is starting')
            for tgid in AdminService.all_ids():
                bot.send_message(tgid, 'Telegram Bot is starting')
            bot.infinity_polling(
                timeout=60,
                long_polling_timeout=60
            )
        except Exception as e:
            logger.error(e)
            for tgid in AdminService.all_ids():
                bot.send_message(tgid, f"Telegram Error [{e}]\n\nRestarting the bot...")
            time.sleep(10)
            for tgid in AdminService.all_ids():
                bot.send_message(tgid, 'Bot restarted successfully')