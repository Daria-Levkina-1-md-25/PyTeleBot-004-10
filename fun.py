# ======================================= 🎢 Развлечения
import requests
import bs4  # BeautifulSoup4
from telebot import types
from io import BytesIO
from datetime import datetime
import random


# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "🦊Лисичка":
        bot.send_photo(chat_id, photo=get_foxURL(), caption="Вот тебе лисичка!")

    elif ms_text == "☀Погода Москва":
        bot.send_message(chat_id, text=weather(chat_id))

    elif ms_text == "🗞Новости":
        bot.send_message(chat_id, text=get_news())

    elif ms_text == "Прислать фильм(A.Ш)":
        send_film(bot, chat_id)

    elif ms_text == "Угадай кто?":
        get_ManOrNot(bot, chat_id)


    elif ms_text == "🎦Фильм(Д)":
        film(bot, chat_id)

    elif ms_text == "💸Valute":
        ans = Valute()
        bot.send_message(chat_id, text=ans)



# -----------------------------------------------------------------------
def send_film(bot, chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


# -----------------------------------------------------------------------
def weather(chat_id):
    req = requests.get('https://sinoptik.ua/погода-москва')
    html = bs4.BeautifulSoup(req.content, "html.parser")

    ans = str(html.select('.today-temp'))
    ans = ans[23:26]
    ans = "Погода на сегодня " + ans
    return ans


# -----------------------------------------------------------------------
def get_news():

    moi_site = requests.get('https://yandex.ru/')
    soup = bs4.BeautifulSoup(moi_site.text, "html.parser")
    result_find = soup.select('.news__item-content')
    array = []

    for result in result_find:
        array.append(result.getText().strip())

    try:
        ans = array[random.randrange(9)]
        return ans
    except IndexError:
        return "Попробуй в другой раз("

# -----------------------------------------------------------------------
def get_foxURL():
    url = ""
    req = requests.get('https://randomfox.ca/floof/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
        # url.split("/")[-1]
    return url


# -----------------------------------------------------------------------
def Valute():
    all_content = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    content = all_content['Valute']

    date = all_content["Date"]
    date = date[:10]
    date = datetime.strptime(date, '%Y-%m-%d')
    date = date.strftime("%m/%d/%Y")

    ans = ""
    ans += "Курс на следующую дату: " + date + "\n"
    ans += str(content['EUR']['Name']) + " " + str(content['EUR']['Value']) + " рублей" + "\n"
    ans += str(content['USD']['Name']) + " " + str(content['USD']['Value']) + " рублей"

    return (ans)

# -----------------------------------------------------------------------
def get_cur_pairs():
    lst_cur_pairs = []
    req_currency_list = requests.get(f'https://currate.ru/api/?get=currency_list&key={SECRET.CURRATE_RU}')
    if req_currency_list.status_code == 200:
        currency_list_json = req_currency_list.json()
        for pairs in currency_list_json["data"]:
            if pairs[3:] == "RUB":
                lst_cur_pairs.append(pairs)
    return lst_cur_pairs


# -----------------------------------------------------------------------
def film(bot, chat_id):
    film = open('фильм.txt', 'r', encoding='UTF-8')
    fact = film.read().split('\n')
    bot.send_message(chat_id, text=random.choice(fact))
    film.close()


# -----------------------------------------------------------------------
def get_ManOrNot(bot, chat_id):

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить", url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")


# ---------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm
