import sys
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import requests

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
        if text == "Taylor Swift":
            taylor = "Muy bien hablemos de Taylor Swift"
            update.message.reply_text(taylor)
            pregunta = update.message.text

            def classify(text):
                key = "417b5f90-9ed1-11eb-b4ba-2fbb5d54afa463763a57-4f98-44de-9c31-be4b40894c61"
                url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

                response = requests.get(url, params={ "data" : text })

                if response.ok:
                    responseData = response.json()
                    topMatch = responseData[0]
                    return topMatch
                else:
                    response.raise_for_status()

            demo = classify(pregunta)

            label = demo["class_name"]
            confidence = demo["confidence"]

            if label == "Album":
                album = ""
                update.message.reply_text(album)

            elif label == "Edad":
                edad = ""
                update.message.reply_text(edad)
            
            elif label == "Genero":
                genero = ""
                update.message.reply_text(genero)
            
            elif label == "Premios":
                premio = ""
                update.message.reply_text(premio)

            elif label == "Extra":
                extra = ""
                update.message.reply_text(extra)

        elif text == "Jeong Han":
            han = "Pregunta sobre Jeong Han"
            update.message.reply_text(han)
            pregunta = update.message.text

            def classify(text):
                key = "417b5f90-9ed1-11eb-b4ba-2fbb5d54afa463763a57-4f98-44de-9c31-be4b40894c61"
                url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

                response = requests.get(url, params={ "data" : text })

                if response.ok:
                    responseData = response.json()
                    topMatch = responseData[0]
                    return topMatch
                else:
                    response.raise_for_status()

            demo = classify(pregunta)

            label = demo["class_name"]
            confidence = demo["confidence"]

            if label == "Album":
                album = ""
                update.message.reply_text(album)

            elif label == "Edad":
                edad = ""
                update.message.reply_text(edad)
            
            elif label == "Genero":
                genero = ""
                update.message.reply_text(genero)
            
            elif label == "Premios":
                premio = ""
                update.message.reply_text(premio)

            elif label == "Extra":
                extra = ""
                update.message.reply_text(extra)
        elif text == "Bad Bunny":
            bunny = "Te contare un poco sobre Bad Bunny"
            update.message.reply_text(bunny)
            pregunta = update.message.text

            def classify(text):
                key = "417b5f90-9ed1-11eb-b4ba-2fbb5d54afa463763a57-4f98-44de-9c31-be4b40894c61"
                url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

                response = requests.get(url, params={ "data" : text })

                if response.ok:
                    responseData = response.json()
                    topMatch = responseData[0]
                    return topMatch
                else:
                    response.raise_for_status()

            demo = classify(pregunta)

            label = demo["class_name"]
            confidence = demo["confidence"]

            if label == "Album":
                album = ""
                update.message.reply_text(album)

            elif label == "Edad":
                edad = ""
                update.message.reply_text(edad)
            
            elif label == "Genero":
                genero = ""
                update.message.reply_text(genero)
            
            elif label == "Premios":
                premio = ""
                update.message.reply_text(premio)

            elif label == "Extra":
                extra = ""
                update.message.reply_text(extra)
        else:
            mal = "Para saber mas de los artistas usa Taylor Swift, Bad Bunny o Jeong Han"
            update.message.reply_text(mal)
    except Exception as e:
        print("Error 002 {}".format(e.args[0]))

def getImage(bot,update):
    try:

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

    while True:
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = tensorflow.keras.models.load_model('keras_model.h5')

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        image = Image.open(image_path)

        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        #turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        resultado = None
        for i in prediction:
                    if i[0] > 0.80:
                        resultado = "El Artista de tu imagen es Taylor Swift"
                    elif i[1] > 0.80:
                        resultado = "El Artista de tu imagen es JeongHan"
                    elif i[2] > 0.80:
                        resultado = "El Artista de tu imagen es Bad Bunny"
                    else:
                        resultado = "No soy tan listo como piensas, prueba con otra imagen"
        print(prediction)
        return resultado

def help(bot,update):
    try:
        message = "Puedo reconocer artistas como Taylor Swift, JeongHan y Bad Bunny"
        update.message.reply_text(message)
        message = "Para una respuesta mas precisa, utiliza imagenes solamente con el rostro y de frente  y con buena calidad"
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