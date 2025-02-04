import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackQueryHandler, Application, ContextTypes, CallbackContext
import os
import whisper
from whisper.utils import get_writer
from datetime import datetime
import requests
from . import twenty_api
from dotenv import load_dotenv

current_dir = os.getcwd()
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN') 
SAVE_DIR_VOICE = os.getenv('SAVE_DIR_VOICE')
SAVE_DIR_TXT = os.getenv('SAVE_DIR_TXT')


# Whisper
model_whisper = whisper.load_model('small')
def get_transcribe(audio: str, language: str = 'nl'):
    return model_whisper.transcribe(audio=audio, language=language, verbose=False)

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# Curent time in readable format
current = datetime.now()
current_time = current.strftime('%Y-%d-%m')



async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# telegram-bot and Whisper
async def download_audio(update: Update, context: CallbackContext):
    audio = update.message.audio or update.message.voice
    txt = update.message.text

    if txt:
        await update.message.reply_text("To use this, please send a voice message. For more information type '/help'.")

    if audio:
        # telegram-bot
        file = await audio.get_file()
        global file_path
        file_path = os.path.join(SAVE_DIR_VOICE, f"{current_time}.ogg")
        await file.download_to_drive(custom_path=file_path)
        await update.message.reply_text("Processing...")

        # Whisper 
        try:
            result = get_transcribe(audio=file_path)
            writer = get_writer("txt", SAVE_DIR_TXT)
            test = writer(result, f"{current_time}.txt")
            
        except Exception as e:
            print(f"Failed to transcribe: {str(e)}")  # Print the actual error
            await update.message.reply_text(f"Failed: {str(e)}")

        await show_option_buttons(update, context)



# Buttons
MENU, BUTTON1, BUTTON2, BUTTON3 = range(4)

async def show_option_buttons(update: Update, context: CallbackContext) -> None:
        
    keyboard = [
        [InlineKeyboardButton("Cancel", callback_data="step_0-button_1")],
        [InlineKeyboardButton("Note", callback_data="step_1-button_1")],
        [InlineKeyboardButton("Task", callback_data="step_1-button_2")],
        [InlineKeyboardButton("Opportunity with Note", callback_data="step_1-button_3")],
        [InlineKeyboardButton("Opportunity with Task", callback_data="step_1-button_4")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome, please choose an option:', reply_markup=reply_markup)

    return MENU

async def button_selection_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    data_dict = query.data.split("-") 
    step = data_dict[0].split("_")[1]
    button = data_dict[1].split("_")[1]

    if step == "0":
        if button == "1":
            await query.edit_message_text(text="Operation is cancelled")
            delete_txt_files()
            return

        
    elif step == "1":
        if button in ["1", "2", "3", "4"]:
            action_map = {"1": "note", "2": "task", "3": "opportunity-note", "4": "opportunity-task"}
            context.user_data["create_type"] = action_map[button]
            await options(update, context)
            await query.edit_message_text(text=f"The {context.user_data['create_type']} is made in twenty.")
            return 
    else:
        return

async def options(update: Update, context: CallbackContext):  
    create_type = context.user_data["create_type"]
    print(create_type)

    if create_type == "note":
        await twenty_api.note(context)
        delete_txt_files()

    elif create_type == "task":
        await twenty_api.task(context)
        delete_txt_files()

    elif create_type == "opportunity-note":
        await twenty_api.note_target(context)
        delete_txt_files()

    elif create_type == "opportunity-task":
        await twenty_api.task_target(context)
        delete_txt_files()
    else:
        return

# python-telegram-bot
def main() -> None:
    os.makedirs(SAVE_DIR_VOICE, exist_ok=True)
    os.makedirs(SAVE_DIR_TXT, exist_ok=True)

    application = Application.builder().token(BOT_TOKEN).build()

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, download_audio))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    application.add_handler(CallbackQueryHandler(button_selection_handler, pattern='^step_'))

    application.run_polling()

if __name__ == "__main__":
    main()
