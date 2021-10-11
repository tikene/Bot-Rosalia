# Importar? pues claro que me importa
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from docsparser import getDriveTable
from time import sleep, gmtime, strftime
from datetime import datetime, timezone, timedelta
import threading
import logging
import pytz
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


bot_token = "" # pruebas
respuesta_string = "Utiliza o comando '/clases' para recibir o horario de hoxe"
root_logs_dir = "User-Logs"
log_file = "logs.txt"
refresh_delay = 500



def logAction(user, action):

    root_path = os.path.join(os.getcwd(), "Telegram_Bot", root_logs_dir)
    username = user[0]

    if not os.path.exists(root_path):
        os.makedirs(root_path)

    userpath = os.path.join(root_logs_dir, username)

    if not os.path.exists(userpath):
        os.makedirs(userpath)

    logfilepath = os.path.join(userpath, log_file)

    if os.path.exists(logfilepath):
        perm = 'a'
    else:
        perm = 'w'


    info = ",".join(user)
    #time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    time = datetime.now(timezone.utc) + timedelta(hours=2)

    with open(logfilepath, perm) as f:
        f.write("[" + time + "]" + "[" + info + "]: " + action + "\n")


def runBot():

    # Setup

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher


    def start(update, context):

        context.bot.send_message(chat_id=update.effective_chat.id, text=respuesta_string)

    def message_reply(update, context):

        user = [
            update["message"]["chat"]["username"],
            update["message"]["chat"]["first_name"],
            update["message"]["chat"]["last_name"]
        ]


        logAction(user, update.message.text)
        print(user, update.message.text)

        context.bot.send_message(chat_id=update.effective_chat.id, text=respuesta_string)

    def clases(update, context):

        dia_semana = datetime.today().weekday()
        tabla_dias = ['LUNS', 'MARTES', 'MÉRCORES', 'XOVES', 'VENRES']
        dia_actual = tabla_dias[dia_semana]
        horario_actual = tablaHorarios[dia_actual]
        clases_hoy = "As túas clases para hoxe, " + dia_actual + "\n"

        for hora in horario_actual:
            if (horario_actual[hora] != ""):
                clases_hoy = clases_hoy + "\n" + hora + " - " + horario_actual[hora]

        user = [
            update["message"]["chat"]["username"],
            update["message"]["chat"]["first_name"],
            update["message"]["chat"]["last_name"]
        ]


        logAction(user, update.message.text)
        print(user, update.message.text)

        context.bot.send_message(chat_id=update.effective_chat.id, text=clases_hoy)



    # Handlers
    start_handler = CommandHandler('start', start)
    clases_handler = CommandHandler('clases', clases)
    message_reply = MessageHandler(Filters.text & (~Filters.command), message_reply)


    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(clases_handler)
    dispatcher.add_handler(message_reply)


    updater.start_polling()

    def refreshDoc():

        savedVersion = False
        results = []

        while True:

            results = getDriveTable(savedVersion)
            tableChanged = results[0]

            if not tableChanged:
                #print("La version del documento no ha cambiado")
                pass
            else:
                savedVersion = tableChanged
                print("Nueva version del documento detectada")
                tablaHorarios = results[1]

            sleep(refresh_delay)

    refresh = threading.Thread(target=refreshDoc).start()

runBot()
