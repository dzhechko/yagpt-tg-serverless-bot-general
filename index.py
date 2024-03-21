import asyncio
import json
import os

#Библиотеки для работы с телеграмм
from telegram import Update, Message, Chat
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

#Библиотеки для YaGPT и Langchain
from yandex_chain import YandexLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Default settings
default_temperature = 0.6
default_context_window = 8000
model_list = [
    "GPT Lite",
    "GPT Pro"      
]    
default_model_index = 1 #используем большую модель YandexGPT

# Current settings
current_temperature = default_temperature
current_context_window = default_context_window
current_model_index = default_model_index

HELP_MESSAGE = """Команды:
⚪ /new – Начать новый диалог
⚪ /mode – Выбрать модель
⚪ /settings – Показать и изменить настройки
⚪ /history – Показать историю беседы
⚪ /help – Показать подсказку

"""

SETTINGS_MESSAGE = """Cуществующие настройки:
⚪ Степень креативности /temperature = {current_temperature}. 
    Допустимый интервал: от 0 до 1
⚪ Размер контектного окна /context = {current_context_window}. 
    Допустимый интервал: от 1000 до 8000
"""

ABOUT_MESSAGE = """

Я бот-помощник, который использует современные LLM модели.
Моя основная задача - отвечать на все твои вопросы, и помогать в решении различных задач.

Типовые сценарии работы со мной - это узнавать разные факты или решать креативные задачи :)
Постараюсь быть максимально полезным!

Ты можешь выбрать LLM-модель, которую хочешь использовать (https://cloud.yandex.ru/ru/docs/yandexgpt/concepts/models).
Можно настроить размер ее контекстного окна и параметры креативности. 
"""


async def new_dialog_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_text = "Контекст предыдущей беседы удален. Можете продолжить общение."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

async def show_chat_modes_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await register_user_if_not_exists(update, context, update.message.from_user)
    # if await is_previous_message_not_answered_yet(update, context): return

    # user_id = update.message.from_user.id
    # db.set_user_attribute(user_id, "last_interaction", datetime.now())
    global model_list, current_model_index
    current_model = model_list[current_model_index]
    message_local = """
    Используется модель {model} (https://cloud.yandex.ru/ru/docs/yandexgpt/concepts/models)
Чтобы поменять модель используй команды:
    /model = lite     для GPT lite
    /model = pro      для GPT pro
    """
    formatted_message = message_local.format(model=current_model)
    reply_text = formatted_message   
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
    # await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

async def show_settings_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_temperature, current_context_window    
    formatted_message = SETTINGS_MESSAGE.format(current_temperature=current_temperature, current_context_window=current_context_window)
    reply_text = formatted_message    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

async def show_history_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_text = "История беседы"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

async def show_help_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_text = ""
    reply_text += ABOUT_MESSAGE
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_text = """
Привет!
Я бот-помощник, который построен на базе GPT-моделей.
Моя основная задача - помочь тебе с ответами на вопросы и с решением креативных задач 
Только не забудь выставить нужную степень моей креативности!
🤖
    """
    reply_text += HELP_MESSAGE

    # await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
    # await show_chat_modes_handle(update, context)

async def set_temperature_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_temperature
    message_text = update.message.text
    if message_text.startswith('/temperature = '):
        value = message_text.split('=')[-1].strip()
    elif message_text.startswith('/temperature '):
        value = message_text.split(' ')[-1].strip()
    temperature = float(value)
    if 0 <= temperature <= 1:
        current_temperature = temperature
    message_local = """
    Текущее значение температуры теперь = {current_temperature}
    """
    formatted_message = message_local.format(current_temperature=current_temperature)
    reply_text = formatted_message    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

async def set_context_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_context_window
    message_text = update.message.text
    if message_text.startswith('/context = '):
        value = message_text.split('=')[-1].strip()
    elif message_text.startswith('/context '):
        value = message_text.split(' ')[-1].strip()
    context = int(value)
    if 1000 <= context <= 8000:
        current_context_window = context
    message_local = """
    Текущее значение размера контекстного окна теперь = {current_context} токенов.
    """
    formatted_message = message_local.format(current_context=current_context_window)
    reply_text = formatted_message    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

async def set_model_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global model_list, current_model_index

    message_text = update.message.text
    if '/model = lite' in message_text or '/model lite' in message_text:
        current_model_index = 0
    elif '/model = pro' in message_text or '/model pro' in message_text:
        current_model_index = 1
    
    current_model = model_list[current_model_index]
    message_local = """
    Текущая LLM-модель, которую используем: {current_model}.
    """
    formatted_message = message_local.format(current_model=current_model)
    reply_text = formatted_message    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

async def process_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_temperature, current_context_window, current_model_index
    # вопрос пользователя
    message_text = update.message.text

    if  message_text == "/start":
        # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
        await start(update, context)
    elif message_text == "/new":
        await new_dialog_handle(update, context)
    elif message_text == "/mode":
        await show_chat_modes_handle(update, context)
    elif message_text == "/settings":
        await show_settings_handle(update, context)
    elif message_text == "/history":
        await show_history_handle(update, context)
    elif message_text == "/help":
        await show_help_handle(update, context)
    elif message_text.startswith("/temperature"):
        await set_temperature_handle(update, context)
    elif message_text.startswith("/context"):
        await set_context_handle(update, context)
    elif message_text.startswith("/model"):
        await set_model_handle(update, context)
    else:
        # обращение к модели YaGPT
        yagpt_folder_id = os.environ["YAGPT_FOLDER_ID"]
        yagpt_api_key = os.environ["YAGPT_API_KEY"]
        yagpt_temperature = current_temperature
        yagpt_max_tokens = current_context_window

        # if current_model_index==0: 
            # model_uri = "gpt://"+str(yagpt_folder_id)+"/yandexgpt-lite/latest"
        # else:
            # model_uri = "gpt://"+str(yagpt_folder_id)+"/yandexgpt/latest"    
        # model = ChatYandexGPT(api_key=yagpt_api_key, model_uri=model_uri, temperature = yagpt_temperature)

        yagpt_prompt = """
        Тебя зовут Яша. Ты очень полезный ИИ-помощник. Отвечай на вопросы коротко и точно. Следуй пожеланиям пользователя, до тех пор пока они не выходят за рамки этики. Если не знаешь ответ, вежливо напиши об этом.
        """
        if current_model_index == 1: bool_lite = False #используем pro модель YandexGPT
        if current_model_index == 0: bool_lite = True  #используем lite модель YandexGPT
        llm = YandexLLM(api_key=yagpt_api_key, folder_id=yagpt_folder_id, temperature = yagpt_temperature, max_tokens=yagpt_max_tokens, use_lite=bool_lite)        
        str2 = """Вопрос: {question}
        Твой ответ:"
        """
        template = f"{yagpt_prompt} {str2}"
        prompt = PromptTemplate(template=template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        response = llm_chain.run({"question": message_text})
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)



bot = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).updater(None).build()

bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("mode", show_chat_modes_handle))

bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process_text_message))

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.initialize())

async def handler(event, context):
    message = json.loads(event["messages"][0]["details"]["message"]["body"])
    update = Update(
        update_id=message["update_id"],
        message=Message(
            message_id=message["message"]["message_id"],
            date=message["message"]["date"],
            chat=Chat(
                id=message["message"]["chat"]["id"],
                type=message["message"]["chat"]["type"]
            ),
            text=message["message"]["text"],
        )
    )

    await bot.process_update(update)

    return {
        "statusCode": 500,
    }
