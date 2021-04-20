import sys
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import requests

token = "1783027747:AAFnkBl8pTAYa9nxls3SqQEXEe380eMwno0"

def start(bot,update): #Instruccion del comando /start
    try:
        username = update.message.from_user.username 
        #saludo que envia el bot
        message = "Hola " + username 
        update.message.reply_text(message)
    except Exception as e:
        print("Error 001 {}".format(e.args[0]))

def echo(bot,update): #Instruccion para responder preguntas
    try:
        pregunta = update.message.text
        respuesta = "Aun no estoy muy bien programado, por lo tanto te respondere de forma mixta la informacion de los 3 artistas que puedo identificar"
        update.message.reply_text(respuesta)

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

        print ("result: '%s' with %d%% confidence" % (label, confidence))

        #aqui evalua en que etiqueta se encuentra el texto enviado y responde segun la etiqueta

        if label == "Album":
                ts1 = "Taylor Swift tiene un total de 11 album (Taylor Swift, Fearless, Speak Now, Red, 1989, Reputation, Lover, Folklore, Evermore, Fearless (Taylor's Version)). "
                update.message.reply_text(ts1)
                yh1 = "Jeong Han, es integrante del grupo SEVENTEEN, tienen un total de 3 album de estudio (Love & Letter, Teen, Age)"
                update.message.reply_text(yh1)
                bb1 = "Bad Bunny tiene un total de 3 album (X 100pre, YHLQMDLG y El ultimo tour del mundo)."
                update.message.reply_text(bb1)

        elif label == "Edad":
                ts2 = "Taylor Swift nació el 13 de Diciembre de 1989, por lo cual al dia de hoy tiene 31 años."
                update.message.reply_text(ts2)
                yh2 = "Jeong Han nació el 4 de Octubre de 1995, por lo cual hoy en día tiene 25 años."
                update.message.reply_text(yh2)
                bb2 = "Bad Bunny nació el 10 de marzo de 1994, por lo que hasta el dia de hoy tiene 27 años."
                update.message.reply_text(bb2)
                
        elif label == "Genero":
                ts3 = "Los primeros 4 discos de Taylor Swift se desarrollan en el genero country, los siguientes 3 son Pop y los 2 mas recientes son Alternativos, es una artista en tres generos: Country, Pop y Alternativo."
                update.message.reply_text(ts3)
                yh3 = "SEVENTEEN maneja una  gran variedad en géneros musicales, pero en los que resaltan más son Pop, Hip-Hop, Funk, R&B y EDM"
                update.message.reply_text(yh3)
                bb3 = "Bad Bunny canta principalmente Trap latino, hip-hop, rap, reguetón, dancehall."
                update.message.reply_text(bb3)
                
        elif label == "Premios":
                ts4 = "Taylor Swift tiene un total de 360 premios, de los cuales los mas importantes son 3 Grammy por Album del año(2009,2015,2021), un AMA por artista de la Decada y Billboard Woman of the Year(2014)."
                update.message.reply_text(ts4)
                yh4 = "SEVENTEEN a ganado un total de 102 premios, de los cuales los más importantes son los MAMA por Worldwide Favorite Artist (2017), Best OST (A-TEEN) (2018), Breakthrough Archivement (2019), Global Performer Artist (2020), Notable Achievement Artist (2020), 2 veces en Best Male Group Dance (2017, 2018),  3 veces en Worldwide Fan’s Choice Top 10 (2018, 2019, 2020)."
                update.message.reply_text(yh4)
                bb4 = "Bad Bunny a ganado un total de 79 premios de los cuales los mas importantes son Compositor del año(2020) y Grammy a mejor album pop latino o urbano(2021)."
                update.message.reply_text(bb4)

        else:
                ts5 = "Taylor Swift: Sus padres son Andrea Swift y Scott Swift, tiene un hermano Austin Swift, tiene 3 gatos Meredith, Olivia y Benjamin. Nacio en Reading, Pennsylvania. Estudio hasta la preparatoria para despues desicarse a la musica. Su disquera actual es Republic Records. Es Cantante-Compositora y Actriz. Su exito es mundial gracias a sus canciones narrativas sobre su vida personal. Su novio actual es el Ingles Joe Alwyn, con el cual lleva 4 años de relacion. Segun Forbes Taylor Swift cuenta con una fortuna de $360 millones de Dolares lo que la posiciona como la 7ma mujer con mayor fortuna en EUA."
                update.message.reply_text(ts5)
                yh5 = "Jeong Han: Nació en Gangbuk-gu, Seúl, Corea del Sur. Tuvo un entrenamiento de 2 años y 2 meses. Es cantante, bailarín, modelo, MC y letrista. A compuesto 7 canciones para el grupo y su modelo a seguir es Teamin de SHINee. Es integrante del grupo SEVENTEEN, su posición es vocalista y bailarín, además él pertenece al Team Vocal "
                update.message.reply_text(yh5)
                bb5 = "Bad Bunny: Benito Antonio Martinez Ocasio nacio en Vega Baja, Puerto Rico. Su madre es Lysaurie Ocasio; tiene dos hermanos: Bernie y Bysael. Su disquera actual es Rimas Entertainment. Tiene un perro llamado Dachshund. Abandono la carrera de Comunicacion Audiovisual pra dedicarse a la musica. Su exitoso se debe rompe los esquemas de muchos cantes urbanos manifestándose en contra de la violencia de genero, las practicas de corrupción en su natal, Puerto Rico e innovar en sus generos. Su novia actual es Gabriela Berlingeri, con quien lleva una relacion de aproximadamente 3 años. Segun Celebrity Neth Worth Bad Bunny asciende a los 16 millones de dólares segun sus ganancias y bienes materiales. "
                update.message.reply_text(bb5)
        
    except Exception as e:
        print("Error 002 {}".format(e.args[0]))

def getImage(bot,update): #Instruccion para identificar imagenes
    try:

        file = bot.getFile(update.message.photo[-1].file_id)
        id = file.file_id

        #Guarda las imagenes

        filename = os.path.join("imagenes/", "{}.jpg".format(id))
        file.download(filename)
        message = "Analizando imagen, espera un momento"
        update.message.reply_text(message)

        #Devuelve la respuesta del analisis

        prediction = analisis(filename)
        print(prediction)
        update.message.reply_text(prediction)

        message = "Esperando otra indicacion"
        update.message.reply_text(message)
    except Exception as e:
        print("Error 003 {}".format(e.args[0]))
    
def analisis (image_path): #Ejecucion del modelo de identificacion de imagenes

    while True:

        np.set_printoptions(suppress=True)

        model = tensorflow.keras.models.load_model('keras_model.h5')

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        image = Image.open(image_path)


        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        image_array = np.asarray(image)

        image.show()

        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        data[0] = normalized_image_array

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
        return resultado #regresa el resultado para ser enviado al usuario

def help(bot,update): #Instrucciones del comando /help
    try:
        message = "Puedo reconocer artistas como Taylor Swift, JeongHan y Bad Bunny."
        update.message.reply_text(message)
        message = "Para una respuesta mas precisa, utiliza imagenes solamente con el rostro y de frente  y con buena calidad."
        update.message.reply_text(message)
        message = "Tengo un poco de informacion sobre los artistas, pregunta cosas como sus discos, edad, premios e informacion extra (Padres, fortuna, mascotas, etc)."
        update.message.reply_text(message)
    except Exception as e:
        print("Error 004 {}".format(e.args[0]))
        
def error(bot,update,e):
    try:
        print(error)
    except Exception as e:
        print("Error 005 {}".format(e.args[0]))

def main(): #Inicia el bot y ejecuta cada una de las instrucciones anteriores
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