from telebot import types
from bot_instance import bot
from water_classes import usrs, admins, orders, comp, AdminService, PhoneNumber, logger
from keybords import Keyboards
from telebot.apihelper import ApiTelegramException

@bot.message_handler(commands=["admin"])
def admin_command(message):
    def mu(message):
        bot.send_message(message.chat.id, f'ℹ* Головне меню*', parse_mode='Markdown', reply_markup=Keyboards.main_menu())
    def admink(message):
        def adding(message):
            if message.text == '↩ Назад':
                admin_panel(message)
            elif len(str(message.text)) in [9,10]:
                try:
                    if int(message.text) in AdminService.all_ids():
                        bot.send_message(message.chat.id, 'Цей користувач вже є адміном!')
                    else:
                        admins.insert_one({'tgid': int(message.text)})
                        bot.send_message(message.chat.id, 'Користувач є адміном ✅')
                        logger.info('User %s has become an admin', message.text)
                        try:
                            bot.send_message(int(message.text),
                                             f'Ви тепер адмін ✅\n\nДля використання введіть /admin')
                        except ApiTelegramException:
                            pass
                    admin_panel(message)
                except TypeError:
                    logger.debug('Incorrect TGID input %s', message.chat.id)
                except Exception:
                    logger.exception('Error accured while adding admin')

        def deleting(message):
            if message.text == '↩ Назад':
                admin_panel(message)
            elif len(str(message.text)) in [9,10]:
                try:
                    if int(message.text) in AdminService.all_ids():
                        admins.delete_one({'tgid': int(message.text)})
                        bot.send_message(message.chat.id, 'Користувач більше не є адміном ✅')
                        logger.info('User %s is not an admin anymore', message.text)
                    else:
                        bot.send_message(message.chat.id, 'Користувач не є адміном!')
                    admin_panel(message)
                except TypeError:
                    logger.debug('Incorrect Telegram ID input %s', message.chat.id)
                except Exception:
                    logger.exception('Error accured while deleting admin')
        def search(message):
            if message.text == '↩ Назад':
                admin_panel(message)
            elif len(message.text) in [9,10]:
                try:
                    user = usrs.find_one({'tgid': int(message.text)})
                    if user:
                        link = f"<a href='tg://user?id={int(message.text)}'>USER</a>"
                        name = bot.get_chat_member(int(message.text), int(message.text)).user.username
                        num = PhoneNumber.phnum(PhoneNumber.get_num(int(message.text)))
                        inline_s = types.InlineKeyboardMarkup()
                        inline_b1 = types.InlineKeyboardButton('🔴Бан', callback_data=f'ban{int(message.text)}')
                        inline_b2 = types.InlineKeyboardButton('🟢Розбан', callback_data=f'unb{int(message.text)}')
                        inline_s.add(inline_b1, inline_b2)
                        bot.send_message(message.chat.id,
                                         f"Користувач\n\nID: <code>{message.text}</code>\nUser: {link}\nUsrname: @{name}\nІм'я: {user['name']}\nТелефон: <code>{num}</code>\nАдреса: {user['adress']}\nЗамовлень: {user['ord']}",
                                         parse_mode='HTML', reply_markup=inline_s)
                    else:
                        bot.send_message(message.chat.id, f'Користувача не знайдено ❌')
                    admin_panel(message)
                except TypeError:
                    logger.debug('Incorrect ID input from %s', message.chat.id)

        def mail_end(message, txt):
            if message.text == 'ПІДТВЕРДИТИ':
                err = 0
                alus2 = 0
                bot.send_message(message.chat.id,
                                 'ℹ Розсилання розпочато\n\nНе користуйтесь ботом, поки не отримаєте повідомлення о закінченні')
                for i in usrs.find({}, {'tgid': 1}):
                    try:
                        bot.send_message(i['tgid'], txt)
                        alus2 += 1
                    except Exception:
                        err+=1
                bot.send_message(message.chat.id,
                                 f"Розсилання завершено\n\n✅ Надіслано:{alus2}\n❌ Заблокували: {err}")
            else:
                bot.send_message(message.chat.id, 'Відхилено')
            admin_panel(message)

        def mailing(message):
            if message.text == "↩ Назад":
                admin_panel(message)
            else:
                k = bot.send_message(message.chat.id, 'Введіть `ПІДТВЕРДИТИ`, щоб продовжити розсилання',
                                     reply_markup=Keyboards.back_button(), parse_mode='Markdown')
                bot.register_next_step_handler(k, mail_end, str(message.text))
        def choosing_admin(message):
            req = list(orders.find({}, {'tgid': 1, 'name': 1, 'num': 1, 'adress': 1, 'val': 1, 'price': 1, 'date': 1,
                                        'type': 1}))
            if message.text == "🟢 Підтвердити":
                completed_req = {'tgid': req[0]["tgid"], 'type': req[0]['type'], 'name': req[0]["name"],
                                 'num': req[0]["num"],
                                 'adress': req[0]["adress"], 'val': req[0]["val"], 'price': req[0]["price"],
                                 'date': req[0]["date"]}
                orders.delete_one(completed_req)
                comp.insert_one(completed_req)
                for us in usrs.find({}, {'_id': 1, 'tgid': 1, "ord": 1}):
                    if us['tgid'] == completed_req['tgid']:
                        usrs.update_one({'tgid': us['tgid']}, {"$set": {'ord': us['ord'] + 1}})
                        break
                name = bot.get_chat_member(completed_req['tgid'], completed_req['tgid']).user.username
                for ad in AdminService.all_ids():
                    bot.send_message(ad,f"<b>ADMIN ALLERT\n\n</b>✅ Замовлення від <code>{completed_req['tgid']}</code> (@{name}) було підтверджено адміном @{bot.get_chat_member(message.chat.id, message.chat.id).user.username}",disable_notification=True,parse_mode='HTML')
                bot.send_message(completed_req['tgid'],'🚀')
                bot.send_message(completed_req['tgid'],
                                 f"*Ваше замовлення підтверджено. Дякуємо за довіру 💫*", parse_mode='Markdown')
                approving_out_admin(message)
            elif message.text == "🔴 Відхилити":
                completed_req = {'tgid': req[0]["tgid"], 'type': req[0]['type'], 'name': req[0]["name"],
                                 'num': req[0]["num"],
                                 'adress': req[0]["adress"], 'val': req[0]["val"], 'price': req[0]["price"],
                                 'date': req[0]["date"]}
                orders.delete_one(completed_req)
                name = bot.get_chat_member(completed_req['tgid'], completed_req['tgid']).user.username
                for ad in AdminService.all_ids():
                    bot.send_message(ad,
                                     f"<b>ADMIN ALLERT\n\n</b>❌ Замовлення від <code>{completed_req['tgid']}</code> (@{name}) було відхилено адміном @{bot.get_chat_member(message.chat.id, message.chat.id).user.username}",disable_notification=True,parse_mode='HTML')
                bot.send_message(completed_req['tgid'],
                                 f"Ваш запит відхилено \nМожливо, Ви надали хибну інформацію або порушили правила нашого бота")
                approving_out_admin(message)
            elif message.text == "↩ Назад":
                admin_panel(message)

        def approving_out_admin(message):
            req = list(orders.find({}, {'tgid': 1, 'name': 1, 'num': 1, 'adress': 1, 'val': 1, 'price': 1, 'date': 1,'type': 1}))
            markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup_ap.add('🟢 Підтвердити', "🔴 Відхилити", "↩ Назад")
            try:
                bot.send_message(message.chat.id,("У вас 1 нове замовлення" if len(req) == 1 else f"У вас {len(req)} нових замовлень"),)
                link = f'<a href="tg://user?id={req[0]["tgid"]}">USER</a>'
                name = bot.get_chat_member(req[0]["tgid"], req[0]["tgid"]).user.username
                if req[0]['type'] is None:
                    req_txt = f"User ID: <code>{req[0]['tgid']}</code>\nUser: @{name}\nІм'я: <code>{req[0]['name']}</code>\nНомер: <code>{PhoneNumber.phnum(req[0]['num'])}</code>\nАдреса: <code>{req[0]['adress']}</code>\nК-сть води: <code>{req[0]['val']}</code>шт\nЦіна: <code>{req[0]['price']}</code>\n\nДата: <code>{req[0]['date']}</code>"
                else:
                    req_txt = f"User ID: <code>{req[0]['tgid']}</code>\nUser: @{name}\nІм'я: <code>{req[0]['name']}</code>\nНомер: <code>{PhoneNumber.phnum(req[0]['num'])}</code>\nАдреса: <code>{req[0]['adress']}</code>\nЦіна: <code>{req[0]['price']}</code>\n\nТовар: <code>{req[0]['type']}</code>"
                bot.send_message(message.chat.id, link, parse_mode='HTML')
                s = bot.send_message(message.chat.id, req_txt, reply_markup=markup_ap, parse_mode='HTML')
                bot.register_next_step_handler(s, choosing_admin)
            except IndexError:
                bot.send_message(message.chat.id, "Запитів немає!")
                admin_panel(message)
        if message.text == '📋 Всі адміни':
            txt = ''
            c = 1
            for i in AdminService.all_ids():
                txt += f'{c}. <a href="tg://user?id={i}"><b>Admin №{c}</b></a>\nID = <code>{i}</code>\n'
                c += 1
            k = bot.send_message(message.chat.id, txt, parse_mode='HTML')
            bot.register_next_step_handler(k, admink)
        elif message.text == '🟢 Додати адміна':
            k = bot.send_message(message.chat.id, 'Введіть TelegramID користувача', reply_markup=Keyboards.back_button())
            bot.register_next_step_handler(k, adding)
        elif message.text == '🔴 Видалити адміна':
            k = bot.send_message(message.chat.id, 'Введіть TelegramID користувача', reply_markup=Keyboards.back_button())
            bot.register_next_step_handler(k, deleting)
        elif message.text == '🔍 Пошук користувача':
            k = bot.send_message(message.chat.id, f'Введіть TelegramID користувача', reply_markup=Keyboards.back_button())
            bot.register_next_step_handler(k, search)
        elif message.text == '📤 Розсилання':
            k = bot.send_message(message.chat.id, 'Напишіть текст для розсилки користувачам 📤',
                                 reply_markup=Keyboards.back_button())
            bot.register_next_step_handler(k, mailing)
        elif message.text == '📄 Замовлення':
            approving_out_admin(message)
        elif message.text == '↩ Головне меню' or message.text == '/start':
            mu(message)
    admink(message)
    def admin_panel(message):
        t = bot.send_message(message.chat.id, 'Оберіть пункт меню:', reply_markup=Keyboards.admin_menu())
        bot.register_next_step_handler(t, admink)
    if int(message.chat.id) in AdminService.all_ids():
        bot.send_message(message.chat.id, '👨‍💻')
        admin_panel(message)
    else:
        bot.send_message(message.chat.id, 'Недостатньо прав ❌')
        mu(message)