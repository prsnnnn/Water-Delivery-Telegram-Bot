# 💧 Aqua Way — Telegram Bot

Telegram-bot service for water delivery — orders managing, products online shop, personal account and fully functional admin-panel for the team.

---

## ✨ Features

### For clients
- 🚰 **Order water delivery** — select the number of bottles with automatic price calculation  (fixed rates, volume-based discounts, negotiable price for large orders)
- 🛒 **Shop** — catalog of pumps (mechanical and electrical), handles, stands, cylinders and taps with photos and descriptions
- 🔑 **Personal account** — profile filling out (name, number, address), check order history
- 📋 **Order history** — status «In progress» and «Done» with details of each order
- 🌍 **Fast-access links** — company website and Instagram link right from the main menu

### For admins
- 👨‍💻 **Admin panel** (`/admin`) — bot management without accessing database directly
- 📄 **Order processing** — approving or rejecting client request in real time
- 👥 **Admin management** — adding, removing, view of admin list
- 🔍 **Client search** — by Telegram ID, with possibility of ban/unban
- 📤 **Mailing** — messages to all bot users
- 🔔 **Auto notification** —  team receives a notification for each new order

---

## 🛠 Tech stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| Telegram API | [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) |
| Database | MongoDB (pymongo) |
| Web-server (keep-alive) | Flask |
| Logging | standard `logging` — console, file (with rotation) and MongoDB |

---

## 📂 Project structure

```
botwater/
├── bot_instance.py     # TeleBot creating a single TeleBot copy
├── botwater.py         # user handlers + entry point 
├── admin_handles.py    # admin-panel and its logic
├── water_classes.py    # business logic: services, MongoDB access
├── keybords.py         # all bot keyboards (reply/inline)
├── logger_setup.py     # logs set up
└── watercfg.py         # real tokens
```

### Main classes (`water_classes.py`)

- **`OrderService`** — order creating and admin notification
- **`PricingService`** — order cost calculation and product catalog
- **`PhoneNumber`** — formatting and getting client phone number
- **`AdminService`** — admin list management

---
---

## 📌 About the project

Developed and maintained by: [Yehor](https://github.com/prsnnnn)
