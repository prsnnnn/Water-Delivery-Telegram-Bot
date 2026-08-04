from pymongo import MongoClient
from watercfg import MONGO_TOKEN
from logger_setup import setup_logging
from telebot.apihelper import ApiTelegramException

mongo = MongoClient(
    MONGO_TOKEN,
    serverSelectionTimeoutMS=5000,
    socketTimeoutMS=20000,
    connectTimeoutMS=20000
)
telebotdb = mongo["Telegrambot"]
usrs = telebotdb["Users"]
bans = telebotdb["Bans"]
admins = telebotdb["Admins"]
orders = telebotdb['Orders']
comp = telebotdb['Completed orders']
logs=telebotdb['Logs']
logger = setup_logging(mongo_collection=logs)

class AdminService:
    @staticmethod
    def all_ids():
        return [a['tgid'] for a in admins.find({}, {'tgid': 1})]
        #return [871076127]
class PricingService:
    FIXED_PRICES = {1: 150, 2: 250, 3: 360, 4: 480}
    @staticmethod
    def calculate(val):
        if val in PricingService.FIXED_PRICES:
            return f'{PricingService.FIXED_PRICES[val]}грн'
        elif 5 <= val < 15:
            return f'{110 * val}грн'
        elif 15 <= val <= 30:
            return 'Договірна'
        return None

    @staticmethod
    def return_catalog():
        return {11: {'d': 'Економ "Lilu" ультрамарин Европідвіс', 'price': 180},
                 12: {'d': 'Економ "Lilu" ультрамарин з краником Европідвіс', 'price': 190},
                 13: {'d': 'Стандарт "Lilu" ультрамирин з наклейкою в кор.', 'price': 195},
                 14: {'d': 'Стандарт "Lilu" Плюс ультрамирин з наклейкою в кор.', 'price': 210},
                 15: {'d': 'Maximum "Lilu" ультрамирин з наклейкою в кор.', 'price': 220},
                 16: {'d': 'Еліт "Lilu" ультрамирин з наклейкою в коробці (океан)', 'price': 230},
                 17: {'d': 'Quick twist блакитна', 'price': 240}, 18: {'d': 'Quick twist чорна', 'price': 240},
                 19: {'d': 'Clover М6', 'price': 180}, 120: {'d': 'Краник для 19л бутелів', 'price': 135},
                 21: {'d': 'Насос для води на батарейках JM-09 (JIUNE)', 'price': 240},
                 22: {'d': 'Clover K3', 'price': 675}, 23: {'d': 'Clover К7', 'price': 265},
                 24: {'d': 'Clover К10', 'price': 435}, 25: {'d': 'Clover К12 (silver)', 'price': 660},
                 26: {'d': 'Clover К15', 'price': 525}, 27: {'d': 'Clover К16', 'price': 375},
                 28: {'d': 'Clover К17', 'price': 265}, 29: {'d': 'Clover К18 блакитна', 'price': 285},
                 210: {'d': 'Clover К18 біла', 'price': 285}, 211: {'d': 'Clover К20 біла', 'price': 375},
                 212: {'d': 'Помпа с аккумулятором Е9 Blue', 'price': 295},
                 213: {'d': 'Помпа с аккумулятором Е12 Gold', 'price': 660},
                 214: {'d': 'Помпа с аккумулятором Е16 зеленая', 'price': 435},
                 215: {'d': 'Помпа с аккумулятором Е18 Violet', 'price': 315},
                 216: {'d': 'Помпа с аккумулятором Е19 синяя', 'price': 360},
                 217: {'d': 'Помпа с аккумулятором Е21', 'price': 375},
                 31: {'d': 'Ручка пластмас. для переносу 19л РС бутелів', 'price': 85},
                 32: {'d': 'Ручка для 19л "Н" синя', 'price': 85},
                 33: {'d': 'Ручка "крюк" для переноса бутылей', 'price': 85},
                 41: {'d': 'Підставка пластик з краником для 19-л бутел.PD-02', 'price': 480},
                 42: {'d': 'Підставка пластик з краником для 19-л бутел.PD-03', 'price': 630},
                 43: {'d': 'Підставка пластикова з краником для 19-літрових бутилів PD-02 L', 'price': 585}}

class PhoneNumber:
    @staticmethod
    def phnum(num):
        s=str(num)
        return f"({s[0:3]})-{s[3:6]}-{s[6:8]}-{s[8:10]}"

    @staticmethod
    def get_num(tgid):
        return usrs.find_one({'tgid': tgid})['num']

class OrderService:
    @staticmethod
    def create(bot, tgid, order_type, price, product_name=None):
        user = usrs.find_one({'tgid': tgid})
        orders.insert_one({
            'tgid': tgid,
            'type': product_name if product_name else order_type,
            'val': None,
            'date': None,
            'name': user["name"],
            'num': user["num"],
            'adress': user["adress"],
            'price': price
        })
        OrderService._notify_admins(bot, tgid)

    @staticmethod
    def _notify_admins(bot, tgid):
        name = bot.get_chat_member(tgid, tgid).user.username
        for admin_id in AdminService.all_ids():
            try:
                bot.send_message(
                    admin_id,
                    f'<b>+1 ЗАМОВЛЕННЯ ТОВАРУ\nTgID: <code>{tgid}</code>\nUsername: @{name}</b>\n\n/admin',
                    parse_mode='HTML'
                )
            except ApiTelegramException:
                pass