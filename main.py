import os
from prettytable import PrettyTable
from telegram.ext import Updater, CommandHandler
from telegram.parsemode import ParseMode

from parse import get_stocks_percents


MAX_MESSAGE_LENGTH = 4096


def start(update, _):
    update.message.reply_text('Здравствуйте!\nЭто бот для получения акций c barchart.com'
                              '\nДля получения акций введите /stocks')


def get_stocks(update, _):
    data = get_stocks_percents(os.getenv('url'))
    if not data:
        return update.message.reply_text('Не удалось произвести поиск')
    data_length = len(data)
    sent_msgs = 0
    table = PrettyTable(['Symbol', 'Volatility'])
    table.align['Symbol'] = 'c'
    table.align['Volatility'] = 'c'
    messages = []
    for i, item in enumerate(data):
        table.add_row(item)
        if len(str(table)) > MAX_MESSAGE_LENGTH:
            table.del_row(-1)
            messages.append(str(table))
            sent_msgs += 1
            table.clear_rows()
            table.header = False
        elif i == data_length - 1:
            messages.append(str(table))
    for msg in messages:
        update.message.reply_text(f'```{msg}```', parse_mode=ParseMode.MARKDOWN_V2)
    update.message.reply_text(f'Total count: {data_length}')


def main():
    updater = Updater(os.getenv('tg_token'))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('stocks', get_stocks))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
