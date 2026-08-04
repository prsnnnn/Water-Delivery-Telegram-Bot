from telebot import types
class Keyboards:
    MAIN_BUTTONS = ['💧 Замовити', '🔑 Мій кабінет', '💰 Ціни',
                     '☎️ Контакти', '🌍 Перейти на сайт', '🖼 Перейти в інстаграм']
    @staticmethod
    def main_menu():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b = Keyboards.MAIN_BUTTONS
        markup.add(b[0], b[1])
        markup.add(b[2], b[3])
        markup.add(b[4], b[5])
        return markup

    @staticmethod
    def admin_menu():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('📄 Замовлення', '📤 Розсилання')
        markup.add('🟢 Додати адміна', '📋 Всі адміни', '🔴 Видалити адміна')
        markup.add('🔍 Пошук користувача')
        markup.add('↩ Головне меню')
        return markup

    @staticmethod
    def back_button():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('↩ Назад')
        return markup

    @staticmethod
    def back_to_main_menu():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('↩ Головне меню')
        return markup

    @staticmethod
    def inline_shop_s1():
        inline_shop = types.InlineKeyboardMarkup()
        inline_b1 = types.InlineKeyboardButton('1️⃣ Економ "Lilu" ультрамарин Европідвіс - 180', callback_data='item11')
        inline_b2 = types.InlineKeyboardButton('2️⃣ Економ "Lilu" ультрамарин з краником Европідвіс - 190',
                                               callback_data='item12')
        inline_b3 = types.InlineKeyboardButton('3️⃣ Стандарт "Lilu" ультрамирин з наклейкою в кор. - 195',
                                               callback_data='item13')
        inline_b4 = types.InlineKeyboardButton('4️⃣ Стандарт "Lilu" Плюс ультрамирин з наклейкою в кор. - 210',
                                               callback_data='item14')
        inline_b5 = types.InlineKeyboardButton('5️⃣ Maximum "Lilu" ультрамирин з наклейкою в кор. - 220',
                                               callback_data='item15')
        inline_b6 = types.InlineKeyboardButton('6️⃣ Еліт "Lilu" ультрамирин з наклейкою в коробці (океан) - 230',
                                               callback_data='item16')
        inline_b7 = types.InlineKeyboardButton('7️⃣ Quick twist блакитна - 240',
                                               callback_data='item17')
        inline_b8 = types.InlineKeyboardButton('8️⃣ Quick twist чорна - 240',
                                               callback_data='item18')
        inline_b9 = types.InlineKeyboardButton('9️⃣ Clover М6 - 180',
                                               callback_data='item19')
        inline_bb = types.InlineKeyboardButton(
            '↩️ Назад', callback_data='shop')
        inline_shop.add(inline_b1)
        inline_shop.add(inline_b2)
        inline_shop.add(inline_b3)
        inline_shop.add(inline_b4)
        inline_shop.add(inline_b5)
        inline_shop.add(inline_b6)
        inline_shop.add(inline_b7)
        inline_shop.add(inline_b8)
        inline_shop.add(inline_b9)
        inline_shop.add(inline_bb)
        return inline_shop

    @staticmethod
    def inline_shop_s2():
        inline_shop = types.InlineKeyboardMarkup()
        inline_b1 = types.InlineKeyboardButton('1️⃣ Насос для води на батарейках JM-09 (JIUNE) - 240',
                                               callback_data='item21')
        inline_b2 = types.InlineKeyboardButton('2️⃣ Clover К3 - 675', callback_data='item22')
        inline_b3 = types.InlineKeyboardButton('3️⃣ Clover К7 - 265', callback_data='item23')
        inline_b4 = types.InlineKeyboardButton('4️⃣ Clover К10 - 435', callback_data='item24')
        inline_b5 = types.InlineKeyboardButton('5️⃣ Clover К12 (silver) - 660', callback_data='item25')
        inline_b6 = types.InlineKeyboardButton('6️⃣ Clover К15 - 525', callback_data='item26')
        inline_b7 = types.InlineKeyboardButton('7️⃣ Clover К16 - 375',
                                               callback_data='item27')
        inline_b8 = types.InlineKeyboardButton('8️⃣ Clover К17 - 265',
                                               callback_data='item28')
        inline_b9 = types.InlineKeyboardButton('9️⃣ Clover К18 блакитна - 285',
                                               callback_data='item29')
        inline_b10 = types.InlineKeyboardButton('1️⃣0️⃣ Clover К18 біла - 285',
                                                callback_data='item210')
        inline_b11 = types.InlineKeyboardButton('1️⃣1️⃣ Clover К20 біла - 375',
                                                callback_data='item211')
        inline_b12 = types.InlineKeyboardButton('1️⃣2️⃣ Помпа с аккумулятором Е9 Blue - 295',
                                                callback_data='item212')
        inline_b13 = types.InlineKeyboardButton('1️⃣3️⃣ Помпа с аккумулятором Е12 Gold - 660',
                                                callback_data='item213')
        inline_b14 = types.InlineKeyboardButton('1️⃣4️⃣ Помпа с аккумулятором Е16 зеленая - 435',
                                                callback_data='item214')
        inline_b15 = types.InlineKeyboardButton('1️⃣5️⃣ Помпа с аккумулятором Е18 Violet - 315',
                                                callback_data='item215')
        inline_b16 = types.InlineKeyboardButton('1️⃣️6️⃣ Помпа с аккумулятором Е19 синяя - 360',
                                                callback_data='item216')
        inline_b17 = types.InlineKeyboardButton('1️⃣7️⃣ Помпа с аккумулятором Е21 - 375',
                                                callback_data='item217')
        inline_bb = types.InlineKeyboardButton(
            '↩️ Назад', callback_data='shop')
        inline_shop.add(inline_b1)
        inline_shop.add(inline_b2)
        inline_shop.add(inline_b3)
        inline_shop.add(inline_b4)
        inline_shop.add(inline_b5)
        inline_shop.add(inline_b6)
        inline_shop.add(inline_b7)
        inline_shop.add(inline_b8)
        inline_shop.add(inline_b9)
        inline_shop.add(inline_b10)
        inline_shop.add(inline_b11)
        inline_shop.add(inline_b12)
        inline_shop.add(inline_b13)
        inline_shop.add(inline_b14)
        inline_shop.add(inline_b15)
        inline_shop.add(inline_b16)
        inline_shop.add(inline_b17)
        inline_shop.add(inline_bb)
        return inline_shop

    @staticmethod
    def inline_shop_s3():
        inline_shop = types.InlineKeyboardMarkup()
        inline_b1 = types.InlineKeyboardButton('1️⃣ Ручка пластмас. для переносу 19л РС бутелiв - 85',
                                               callback_data='item31')
        inline_b2 = types.InlineKeyboardButton('2️⃣ Ручка для 19л "Н" синя - 85', callback_data='item32')
        inline_b3 = types.InlineKeyboardButton('3️⃣ Ручка "крюк" для переноса бутылей - 85', callback_data='item33')
        inline_bb = types.InlineKeyboardButton(
            '↩️ Назад', callback_data='shop')
        inline_shop.add(inline_b1)
        inline_shop.add(inline_b2)
        inline_shop.add(inline_b3)
        inline_shop.add(inline_bb)
        return inline_shop

    @staticmethod
    def inline_shop_s4():
        inline_shop = types.InlineKeyboardMarkup()
        inline_b1 = types.InlineKeyboardButton('1️⃣ Підставка пластик з краником для 19-л бутел.PD-02 - 480',
                                               callback_data='item41')
        inline_b2 = types.InlineKeyboardButton('2️⃣ Підставка пластик з краником для 19-л бутел.PD-03 - 630',
                                               callback_data='item42')
        inline_b3 = types.InlineKeyboardButton(
            '3️⃣ Підставка пластикова з краником для 19-літрових бутилів PD-02 L - 585', callback_data='item43')
        inline_b4 = types.InlineKeyboardButton(
            '4️⃣ Підставка металева для 19-літрових бутелів(чорн) - 90', callback_data='item44')
        inline_b5 = types.InlineKeyboardButton(
            '5️⃣ Подставка хром - 450', callback_data='item45')
        inline_bb = types.InlineKeyboardButton(
            '↩️ Назад', callback_data='shop')
        inline_shop.add(inline_b1)
        inline_shop.add(inline_b2)
        inline_shop.add(inline_b3)
        inline_shop.add(inline_b4)
        inline_shop.add(inline_b5)
        inline_shop.add(inline_bb)
        return inline_shop

    @staticmethod
    def inline_shop_catalog():
        inline_shop = types.InlineKeyboardMarkup()
        inline_b1 = types.InlineKeyboardButton('1️⃣ Механічні помпи', callback_data='i1')
        inline_b2 = types.InlineKeyboardButton('2️⃣ Електрична помпа', callback_data='i2')
        inline_b3 = types.InlineKeyboardButton('3️⃣ Ручки', callback_data='i3')
        inline_b4 = types.InlineKeyboardButton('4️⃣ Підставки', callback_data='i4')
        inline_b5 = types.InlineKeyboardButton('5️⃣ Балон', callback_data='balon')
        inline_b6 = types.InlineKeyboardButton('6️⃣ Краник', callback_data='item120')
        inline_b7 = types.InlineKeyboardButton('📸 Фотокаталог', callback_data='vip',
                                               url='https://teletype.in/@waffy/aquaway_catalog')
        inline_shop.add(inline_b1)
        inline_shop.add(inline_b2)
        inline_shop.add(inline_b3)
        inline_shop.add(inline_b4)
        inline_shop.add(inline_b5)
        inline_shop.add(inline_b6)
        inline_shop.add(inline_b7)
        return inline_shop

    @staticmethod
    def inline_shop_pompa(callback):
        inline_shop = types.InlineKeyboardMarkup()
        inline_b2 = types.InlineKeyboardButton('↩ Назад', callback_data='shopback')
        inline_b1 = types.InlineKeyboardButton('💲 Замовити', callback_data=f'pompa{list(callback)[-1]}buy')
        inline_shop.add(inline_b1)
        inline_shop.add(inline_b2)
        return inline_shop

    @staticmethod
    def order_inline():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('💧 Замовити доставку води', '🛒 Перейти в магазин')
        markup.add('↩ Назад')
        return markup

    @staticmethod
    def personal_cabinet():
        inline_cab = types.InlineKeyboardMarkup()
        inline_b1 = types.InlineKeyboardButton('🔄Заповнити інформацію', callback_data='cab')
        inline_b2 = types.InlineKeyboardButton('📋Історія замовлень', callback_data='history')
        inline_b3 = types.InlineKeyboardButton('🛒Магазин', callback_data='shop')
        inline_cab.add(inline_b3)
        inline_cab.add(inline_b2)
        inline_cab.add(inline_b1)
        return inline_cab

    @staticmethod
    def website_inline():
        inline_k = types.InlineKeyboardMarkup()
        inline_bt = types.InlineKeyboardButton(f"🌈 Перейти на вебсайт", parse_mode='Markdown',
                                               callback_data='vip',
                                               url=f'https://aqua-way.dp.ua/')
        inline_k.add(inline_bt)
        return inline_k

    @staticmethod
    def insta_inline():
        inline_k = types.InlineKeyboardMarkup()
        inline_bt = types.InlineKeyboardButton(f"🌈 Перейти в інстаграм", parse_mode='Markdown',
                                               callback_data='vip',
                                               url=f'https://www.instagram.com/aqua_way.dp?igsh=MTRyOHR6bjMydHg2dQ==')
        inline_k.add(inline_bt)
        return inline_k