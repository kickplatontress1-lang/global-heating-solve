import telebot
from openai import OpenAI

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('token')
client = OpenAI(
    api_key="apikey", # noqa
    base_url="https://api.groq.com/openai/v1",
)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open("hello.jpeg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="👋Привет, этот бот получает информацию о глобальном потеплении и рассказывает факты о нём.\n\n⚡Команды:\n/facts - Получить случайный факт о глобальном потеплении\n/help - Что делать при глобальном потеплении\n\nИли напишите сообщение, чтобы получить помощь от ИИ") # noqa


@bot.message_handler(commands=['facts'])
def send_fact(message):
    facts = [
        "💡Глобальное потепление приводит к повышению уровня моря.",
        "💡Средняя температура Земли увеличилась примерно на 1°C с конца XIX века.", # noqa
        "💡Ледники тают, что приводит к изменению экосистем.",
        "💡Глобальное потепление влияет на здоровье человека, вызывая тепловые удары и болезни.", # noqa
        "💡Изменение климата может привести к экстремальным погодным условиям."
    ]
    import random
    fact = random.choice(facts)
    bot.reply_to(message, fact + "\nВы можете изучить больше фактов о глобальном потеплении, используя команду /facts") # noqa


@bot.message_handler(commands=['help'])
def send_help(message):
    with open("solve.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="❓Если вы хотите помочь в борьбе с глобальным потеплением, вы можете:\n" # noqa
                                                       "-♻️Сократить использование пластика\n" # noqa
                                                       "-🚌Использовать общественный транспорт или велосипед\n" # noqa
                                                       "-💡Экономить электроэнергию\n" # noqa
                                                       "-🌱Поддерживать экологические инициативы") # noqa


@bot.message_handler(func=lambda message: True)
def send_ai_info(message):
    response = client.responses.create(
        input="Я отправил вопрос про глобальное потепление, а вы отвечайте покороче и не более 4096 символов: " + message.text, # noqa
        model="openai/gpt-oss-20b",
    )
    bot.reply_to(message, response.output_text, parse_mode='Markdown')


bot.polling()
