# Telegram Sales Bot

A Telegram bot for browsing a product catalog, adding items to a cart, and
checking out. Admins get a message for every new order and can manage
products via chat commands. Built with `python-telegram-bot` and SQLite.

## What it does

- `/start` — first-time users pick a language (🇬🇧 English, 🇨🇳 中文, 🇸🇦 العربية, 🇻🇳 Tiếng Việt), then see a main menu
- `/menu` — recall the main menu anytime (Catalog / Cart / Language / Help buttons)
- Telegram's native "/" menu button also lists all commands (set automatically on startup)
- `/catalog` — browse products by category (inline buttons, with photos)
- `/cart` — view cart, checkout or clear it
- `/language` — change language anytime; the choice is saved per user in the database, so it's remembered across sessions
- Checkout collects name, phone, and delivery address, then confirms — all in the customer's chosen language
- Admin gets notified of every order in their own Telegram chat (admin messages stay in English)
- Admin commands: `/addproduct`, `/listproducts`, `/removeproduct`, `/orders`

---

## 1. Create your bot with BotFather

1. Open Telegram, search for **@BotFather**, and start a chat.
2. Send `/newbot` and follow the prompts (choose a name and a username
   ending in `bot`).
3. BotFather gives you a **token** like `123456789:AAExampleToken...`.
   Save it — you'll need it in step 3.

## 2. Find your admin chat ID

This lets the bot notify *you* when an order comes in, and unlocks admin
commands for your account.

1. Search for **@userinfobot** on Telegram and start it.
2. It replies with your numeric user ID (e.g. `987654321`). Save it.

## 3. Run it locally

```bash
# from inside the telegram_shop_bot folder
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# now edit .env and paste in your real BOT_TOKEN and ADMIN_CHAT_ID
```

Add a few test products (optional):

```bash
python seed_products.py
```

Start the bot:

```bash
python bot.py
```

Open Telegram, find your bot by its username, and send `/start`. Try
`/catalog`, add something to your cart, and check out. Your admin chat
should get an order notification.

## 4. Add real products

As the admin, message your bot:

```
/addproduct Blue Mug | Ceramic, 350ml | 12.50 | https://example.com/mug.jpg | Kitchen | 20
```

Format: `Name | Description | Price | ImageURL | Category | Stock`
(leave ImageURL blank between the `|` characters if you don't have one yet).

Use `/listproducts` to see IDs, `/removeproduct <id>` to delete one. Stock
count goes down automatically each time an order is placed for that item,
and customers see how many are left when browsing the catalog.

### Starter catalog

Run `python seed_products.py` to load 6 ready-made products (shirt,
trousers, plate set, shoes, sun hat, cap — all in USD with stock counts).
Edit the `products` list at the top of that file to change names, prices,
or quantities before running it, or just use `/addproduct` in the bot to
add your own from scratch.

### Bulk import by uploading a file

Instead of typing `/addproduct` one at a time, the admin can upload a
`.txt` or `.csv` file directly in the Telegram chat with the bot — one
product per line, same pipe-delimited format:

```
Name | Description | Price | ImageURL | Category | Stock
```

A ready-made file with the 6 starter products is included as
`products.txt` — just attach it in the chat with your bot (paperclip icon
→ File) and send. The bot reads it and adds every line as a product,
then replies with how many were added and lists any lines it couldn't
parse. Lines starting with `#` are treated as comments and skipped.

This is the fastest way to (re)load your catalog after a redeploy wipes
the database (see the note on ephemeral storage above) — keep
`products.txt` handy and just re-upload it.

---

## 5. Deploying (Render, free tier)

The bot runs as a **background worker** (it polls Telegram for updates —
no public URL needed).

1. Push this folder to a GitHub repository.
2. Go to [render.com](https://render.com) → **New** → **Background Worker**.
3. Connect your GitHub repo.
4. Settings:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python bot.py`
5. Under **Environment**, add:
   - `BOT_TOKEN` = your token from BotFather
   - `ADMIN_CHAT_ID` = your Telegram user ID
6. Deploy. Check the logs for `Bot starting...` — then message your bot
   on Telegram to confirm it responds.

### Notes on the free tier
- Render's free background workers may spin down after inactivity on
  some plans — check current limits, since these change. If your bot
  needs to be always-on, a small paid worker instance is more reliable.
- SQLite (`shop.db`) is stored on the worker's local disk. On most free
  tiers this disk is **ephemeral** — it resets on redeploy. For
  anything beyond testing, either upgrade to a plan with a persistent
  disk, or swap SQLite for a managed database (Render/Railway both
  offer free Postgres tiers) once you're ready — ask me and I can help
  you migrate `database.py` to Postgres.

### Alternative: Railway or Fly.io
Same idea — deploy as a worker/background process (not a web service),
set `BOT_TOKEN` and `ADMIN_CHAT_ID` as environment variables, start
command `python bot.py`. Both have similar free-tier caveats around
persistent storage and sleep/inactivity — check their current docs
before you commit real order data to it.

---

## 6. Customizing further

Ideas for next steps, happy to help with any of these:
- Payment integration (Stripe, Paystack, M-Pesa, etc.) at checkout
- Persisting the cart in the database instead of memory (survives restarts)
- Order status updates sent back to the customer (e.g. "shipped")
- A simple admin web dashboard instead of chat commands
- Migrating from SQLite to Postgres for reliable free-tier hosting
- Adding more languages — open `translations.py`, add an entry to `LANGUAGES`
  with a flag/name, then copy the `"en"` block in `TRANSLATIONS` and translate
  each value
- Right-to-left layout polish for Arabic (Telegram handles RTL text
  automatically, but double-check button label lengths look right)

## File overview

```
telegram_shop_bot/
├── bot.py              # main bot logic and handlers
├── database.py         # SQLite schema and queries
├── seed_products.py    # optional sample data
├── requirements.txt
├── Procfile             # tells Render/Railway how to start the worker
├── .env.example
└── .gitignore
```
