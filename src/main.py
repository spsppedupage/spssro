import requests
import time
import threading
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

URL = "https://t-t.sps-sro.sk/result.php?cmd=VERKNR_SEARCH&sprache=E&km_mandnr=1&kundenr=33564&verknr=SK0SA2Y510000SXWWC"

BOT_TOKEN = "8666108955:AAFOEFIkIjegpwlqNYVyeKK5WMWmA_uyFuA"
CHAT_ID = 7667560786
USER_ID = 7667560786  # tvoje Telegram ID

last_status = None

def get_status():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()

    for line in text.split("\n"):
        if "Status" in line or "Shipment" in line:
            return line.strip()

    return "Status nenajdeny"

async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = get_status()
    await update.message.reply_text(f"📦 Aktualny status:\n\n{status}")

def send_msg(app, text):
    app.bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="HTML"
    )

def monitor(app):
    global last_status

    last_status = get_status()

    while True:
        time.sleep(60)
        new_status = get_status()

        if new_status != last_status:
            send_msg(
                app,
                f"🚨 <b>ZMENA STATUSU!</b>\n\n"
                f"👤 <a href='tg://user?id={USER_ID}'>@cocainehead</a>\n\n"
                f"⬅️ Stary:\n{last_status}\n\n"
                f"➡️ Novy:\n{new_status}"
            )

            last_status = new_status

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("view", view))

    threading.Thread(target=monitor, args=(app,), daemon=True).start()

    print("Bot bezi...")
    app.run_polling()

if __name__ == "__main__":
    main()
