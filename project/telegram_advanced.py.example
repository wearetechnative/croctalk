import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackQueryHandler, Application, ContextTypes, CallbackContext, ConversationHandler, TypeHandler
import os
import whisper
from whisper.utils import get_writer
from datetime import datetime
import requests
import twenty_query
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN') 

SAVE_DIR_VOICE = "voice/"
SAVE_DIR_TXT = "txt/"

# Whisper
model_whisper = whisper.load_model('small')
def get_transcribe(audio: str, language: str = 'nl'):
    return model_whisper.transcribe(audio=audio, language=language, verbose=False)

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger()
logger = logging.getLogger(__name__)


# Curent time in readable format
current = datetime.now()
current_time = current.strftime('%Y-%d-%m')


# Buttons
MENU, WAITING_FOR_AUDIO, WAITING_FOR_TXT, SELECT = range(4)

async def help(update: Update, context: CallbackContext):
    help_text = (
        "Welcome to the Twenty Bot! Here's what you can do:\n\n"
        "1. Send a Voice Message: Speak your note, task, or opportunity and send it as a voice message.\n"
        "   - The bot will process your voice and transcribe it into text.\n\n"
        "2. Choose an Action:\n"
        "   - After transcription, you'll be presented with 3 options:\n"
        "     - New Note: Save your transcribed message as a note.\n"
        "     - New Task: Save your transcribed message as a task.\n"
        "     - New Opportunity: Save your transcribed message as an opportunity.\n\n"
        "3. Cancel Option:\n"
        "   - If you change your mind, you can cancel the operation.\n\n"
        "For more assistance contact your administrator."
    )
    await update.message.reply_text(help_text)

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Cancel", callback_data="step_0-button_1")],
        [InlineKeyboardButton("New Note", callback_data="step_1-button_1")],
        [InlineKeyboardButton("New Task", callback_data="step_1-button_2")],
        [InlineKeyboardButton("New Opportunity", callback_data="step_1-button_3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to CrocTalk, what would you like to create for twenty:', reply_markup=reply_markup)

    return MENU


async def step_two(update: Update, context: CallbackContext, create_type="") -> int:
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="step_2-button_1")],
        [InlineKeyboardButton("No", callback_data="step_2-button_2")],
        [InlineKeyboardButton("Cancel", callback_data="step_0-button_1")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Do you want to give the "+context.user_data["create_type"]+" a name?", reply_markup=reply_markup)

    return MENU

async def step_three(update: Update, context: CallbackContext):
    txt = update.message.text

    if not txt:
        await update.message.reply_text("Please type the name.")
        return WAITING_FOR_AUDIO

    context.user_data["typed_name"] = txt

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="step_3-button_1")],
        [InlineKeyboardButton("No", callback_data="step_3-button_2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
 
    await update.message.reply_text(f"Do you want to name it: {txt}?", reply_markup=reply_markup)

    return MENU

async def listen_audio(update: Update, context: CallbackContext):
   audio = update.message.audio or update.message.voice

   if not audio:
        await update.message.reply_text("Please send a voice message.")
        return WAITING_FOR_AUDIO  
    
   file = await audio.get_file()
   file_path = os.path.join(SAVE_DIR_VOICE, f"{current_time}.ogg")
   await file.download_to_drive(custom_path=file_path) 

   try:
        result = get_transcribe(audio=file_path)
        writer = get_writer("txt", SAVE_DIR_TXT)
        writer(result, f"{current_time}.txt")

        create_type = context.user_data.get("create_type", "unknown")
        await update.message.reply_text(f"Your {create_type} has been processed successfully!")

        return await step_two(update, context, create_type)

   except Exception as e:
        logger.error(f"Transcription failed: {e}")
        await update.message.reply_text("Failed to transcribe the message.")
        return WAITING_FOR_AUDIO  

async def button_selection_handler(update: Update, context: CallbackContext, create_type="") -> int:
    query = update.callback_query
    await query.answer()

    data_dict = query.data.split("-") 
    step = data_dict[0].split("_")[1]  # Extract step number
    button = data_dict[1].split("_")[1]  # Extract button number


    if step == "0":
        if button == "1":
            await query.edit_message_text(text="Operation is cancelled")
            delete_txt_files()
            return ConversationHandler.END

        
    elif step == "1":
        if button in ["1", "2", "3"]:
            action_map = {"1": "note", "2": "task", "3": "opportunity"}
            context.user_data["create_type"] = action_map[button]
            await query.edit_message_text(text=f"Please send a voice message for your {context.user_data['create_type']}.")
            return WAITING_FOR_AUDIO

    elif step == "2":
        if button == "1":
            await query.edit_message_text(text=f"Type the name for {context.user_data['create_type']}.")
            return WAITING_FOR_TXT

        if button == "2":
            await query.edit_message_text(text="Proceeding...")
            return

        return ConversationHandler.END
        
    elif step == "3":
        if button == "1":
            name = context.user_data.get("typed_name", "Unnamed")
            await query.edit_message_text(f"Name confirmed: {name}")
            return SELECT

        if button == "2":
            await query.edit_message_text("Please type a new name.")
            return WAITING_FOR_TXT  

    return ConversationHandler.END

async def options(update: Update, context: CallbackContext):  
    create_type = context.user_data["create_type"]
    print(create_type)

    if create_type == "note":
        await twenty_query.note()
        delete_txt_files()

    if create_type == "task":
        await twenty_query.task()
        delete_txt_files()

    if create_type == "opportunity":
        await twenty_query.opportunity()
        await twenty_query.note()
        await twenty_query.note_target()
        delete_txt_files()

# Function to delete files in txt folder
def delete_txt_files():
    files_txt = os.listdir(SAVE_DIR_TXT)
    files_voice = os.listdir(SAVE_DIR_VOICE)
    for file in files_txt:
        file_path_txt = os.path.join(SAVE_DIR_TXT, file)
        os.remove(file_path_txt)
        logger.info(f"Deleted file: {file_path_txt}")
    for file in files_voice:
        file_path_voice = os.path.join(SAVE_DIR_VOICE, file)
        os.remove(file_path_voice)
        logger.info(f"Deleted file: {file_path_voice}")

def main() -> None:
    os.makedirs(SAVE_DIR_VOICE, exist_ok=True)
    os.makedirs(SAVE_DIR_TXT, exist_ok=True)

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [CallbackQueryHandler(button_selection_handler, pattern='^step_')],
            WAITING_FOR_AUDIO: [MessageHandler(filters.VOICE | filters.AUDIO, listen_audio)],
            WAITING_FOR_TXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, step_three)],
            #SELECT: [TypeHandler(options)]
        },
        fallbacks=[CommandHandler('cancel', help)]
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
