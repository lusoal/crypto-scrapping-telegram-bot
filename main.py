from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
import telegram
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start_bot():
    updater = Updater(token=os.getenv('TELEGRAM_TOKEN',''), use_context=True)
    dispatcher = updater.dispatcher

    return dispatcher, updater


def cripto(update, context):

    DRIVER_PATH = './chromedriver'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    # This is the current crypto list that we are scrapping, more can be added
    crypto_list = ["prices-bitcoin", "prices-ethereum"]

    for crypto in crypto_list:
        print(f"{crypto}")
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(f"https://br.tradingview.com/markets/cryptocurrencies/{crypto}/")
        time.sleep(10)
        html = driver.page_source

        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        list_classes = [{"Venda" : "tv-screener-table__signal tv-screener-table__signal--sell"},
            {"Venda Forte" : "tv-screener-table__signal tv-screener-table__signal--strong-sell"},
            {"Compra Forte" : "tv-screener-table__signal tv-screener-table__signal--strong-buy"}, 
            {"Compra" : "tv-screener-table__signal tv-screener-table__signal--buy"},
            {"Neutro" : "tv-screener-table__signal tv-screener-table__signal--neutral"}]

        message = ""
        best_tip = 0
        tip = ""

        for classes in list_classes:
            label = list(classes.keys())[0]
            label_value = list(classes.values())[0]
            
            span = list(soup.find_all('span', class_=label_value))
            # print(label, len(span))

            oportunity = len(span)
            message += f"*{label}:* {oportunity}\n"

            # Verificar qual é a melhor dica baseado na moeda
            if oportunity > best_tip:
                best_tip = oportunity
                tip = f"*A dica é {label}*"

        if ("Compra" or "Compra Forte") in tip:
            tip += " {}".format("\u2705")
        if ("Venda" or "Venda Forte") in tip:
            tip += " {}".format("\u274C")

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"*Moeda:* {crypto}\n\n{message}\n{tip}", 
            parse_mode=telegram.ParseMode.MARKDOWN)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Eu sou o Cripto Bot, pergunte */cripto*", 
        parse_mode=telegram.ParseMode.MARKDOWN)


def main():
    dispatcher, updater = start_bot()

    # Commands that bot can respond
    # TODO: Refactoring handler and functions
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    cripto_handler = CommandHandler('cripto', cripto)
    dispatcher.add_handler(cripto_handler)

    updater.start_polling()
    
if __name__ == '__main__':
    main()
    