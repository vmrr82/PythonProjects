from ast import Call
from asyncore import dispatcher
from email import message
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler
import logging
import pandas as pd

tokenBot = '5117214155:AAHvxsDe3HKh55kAgRduGJ-kebB-xGLyhsY'
updater = Updater(token=tokenBot,use_context= True) #Actualizaciones

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO) #Función rescata errores

df = pd.read_csv('LectorPDF\Codificado-DGT-3-de-septiembre-de-2021.csv',delimiter=',',encoding='utf-8').fillna(value=0)

def start(update: Updater, context: CallbackContext):
    start_text = "Bienvenido al Codificado de Tráfico NO OFICIAL de la DGT.\nEstos son los comandos disponibles: \n/help - Ayuda. \n/consulta - búsqueda de definiciones."
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_text) #Mensaje /Start

def consulta(update: Updater,context: CallbackContext):
    
    consultaUsuario = context.args[0]
    buscarInfraccion = df[df.TEXTO_HECHO_INFRINGIDO.str.contains(consultaUsuario,case=False,na=False)].to_csv(sep=',')
    if buscarInfraccion:
        update.message.reply_text(buscarInfraccion)
        print(consultaUsuario)
    else:
        update.message.reply_text("Articulo no encontrado")
        print(consultaUsuario)

def help(update:Updater,context: CallbackContext): #Funcion de ayuda del bot
    help_text = "Para usar este buscador realiza la siguiente búsqueda.\nEj.: /consulta cinturón. Saldrán todos las coincidencias disponibles en el códificado."
    context.bot.send_message(chat_id= update.effective_chat.id,text=help_text)

def title(update:Updater,context:CallbackContext): #Limpiar mensajes
    nuevo_titulo = context.args[0]
    context.bot.set_chat_title(chat_id = update.effective_chat.id,title=nuevo_titulo)

def comandos(update:Updater,context:CallbackContext):
    context.bot.get_my_commands()

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help',help))
dispatcher.add_handler(CommandHandler('consulta',consulta))
dispatcher.add_handler(CommandHandler('title',title))
dispatcher.add_handler(CommandHandler('comandos',comandos))
updater.start_polling() #Inicia Bot
updater.idle()

if __name__ == "__main__":
    bot = telegram.Bot(token=tokenBot)
    print(bot.getMe())
    
    