import sys
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

token = "1783027747:AAFnkBl8pTAYa9nxls3SqQEXEe380eMwno0"

def start(bot,update):
    try:
        username = update.message.from_user.username
        message = "Hola " + username
        update.message.reply_text(message)
    except Exception as e:
        print("Error 001 {}".format(e.args[0]))

def echo(bot,update):
    try:
        text = update.message.text
        update.message.reply_text(text)
    except Exception as e:
        print("Error 002 {}".format(e.args[0]))

def getImage(bot,update):
    try:
        message = "Recibiendo imagen"
        update.message.reply_text(message)

        file = bot.getFile(update.message.photo[-1].file_id)
        id = file.file_id

        filename = os.path.join("imagenes/", "{}.jpg".format(id))
        file.download(filename)
        message = "Analizando imagen, espera un momento"
        update.message.reply_text(message)

        prediction = analisis(filename)
        print(prediction)
        update.message.reply_text(prediction)

        message = "Esperando otra indicacion"
        update.message.reply_text(message)
    except Exception as e:
        print("Error 003 {}".format(e.args[0]))
    
def analisis (image_path):
        np.set_printoptions(suppress=True)

        model = tensorflow.keras.models.load_model('keras_model.h5')

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        prediction = model.predict(data)
        resultado = None
        for i in prediction:
                    if i[0] > 0.43:
                        resultado = "El Artista de tu imagen es Taylor Swift"
                    elif i[1] > 0.43:
                        resultado = "El Artista de tu imagen es JeongHan"
                    elif i[2] > 0.43:
                        resultado = "El Artista de tu imagen es Bad Bunny"
                    elif i[0]:
                        resultado = "No soy tan listo como piensas, prueba con otra imagen"
                    elif i[1]:
                        resultado = "No soy tan listo como piensas, prueba con otra imagen"
                    elif i[2]:
                        resultado = "No soy tan listo como piensas, prueba con otra imagen"
        print(prediction)
        return resultado

def help(bot,update):
    try:
        message = "Pedrito prometo no ver nada de tu telefono.Era solo una broma :("
        update.message.reply_text(message)
    except Exception as e:
        print("Error 004 {}".format(e.args[0]))
        
def error(bot,update,e):
    try:
        print(error)
    except Exception as e:
        print("Error 005 {}".format(e.args[0]))

def main():
    try:
        updater = Updater(token)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start",start))
        dp.add_handler(CommandHandler("help",help))

        dp.add_handler(MessageHandler(Filters.text,echo))
        dp.add_handler(MessageHandler(Filters.photo, getImage))

        dp.add_error_handler(error)

        updater.start_polling()
        updater.idle()
    except Exception as e:
        print("Error 006 {}".format(e.args[0]))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error 007 {}".format(e.args[0])) 