from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

API_KEY = 'f08e6acb6882e82208e706fd5f05f663'
OPENWEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

OUTFITS_DATABASE = {
    'walk_снег': {
        'name': 'Зимняя прогулка в стиле',
        'description': 'Теплый пуховик, свитер, термобелье, водонепроницаемые ботинки. Идеально для снежной погоды!',
        'image': 'https://www.pressfoto.ru/image-8942704',
        'clothes': 'Пуховик, свитер, термобелье, ботинки',
        'accessories': 'Шарф, шапка, перчатки'
    },
    'walk_дождь': {
        'name': 'Стиль в дождливый день',
        'description': 'Непромокаемое пальто-тренч, водолазка, джинсы, резиновые сапоги. Сухо и модно!',
        'image': 'https://via.placeholder.com/400x300/4ECDC4/FFFFFF?text=Дождливая+прогулка',
        'clothes': 'дождевик, водолазка, джинсы, сапоги',
        'accessories': 'Зонт, шапка-бини'
    },
    'walk_прохладно': {
        'name': 'Уютный осенний лук',
        'description': 'Свитшот-оверсайз, джинсы-скинни, кеды. Отлично для прохладной погоды!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Прохладная+прогулка',
        'clothes': 'Свитшот, джинсы, кеды',
        'accessories': 'Легкая куртка, рюкзак'
    },
    'walk_тепло': {
        'name': 'Легкий летний лук',
        'description': 'Футболка-оверсайз, шорты-бермуды, кеды. Комфортно в теплый день!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Теплая+прогулка',
        'clothes': 'Футболка, шорты, кеды',
        'accessories': 'Солнечные очки, кепка'
    },

    'event_снег': {
        'name': 'Элегантный зимний лук',
        'description': 'Шерстяное пальто, костюм, водолазка, кожаные ботинки. Строго и тепло!',
        'image': 'https://via.placeholder.com/400x300/45B7D1/FFFFFF?text=Зимнее+мероприятие',
        'clothes': 'Пальто, костюм, водолазка, ботинки',
        'accessories': 'Шарф, перчатки, портфель'
    },
    'event_дождь': {
        'name': 'Деловой лук в дождь',
        'description': 'Классический плащ, рубашка, брюки, туфли. Стильно и защищено от дождя!',
        'image': 'https://via.placeholder.com/400x300/4ECDC4/FFFFFF?text=Мероприятие+дождь',
        'clothes': 'Плащ, рубашка, брюки, туфли',
        'accessories': 'Зонт, кожаный портфель'
    },
    'event_прохладно': {
        'name': 'Стильный лук в прохладу',
        'description': 'Пиджак, водолазка, брюки, ботинки. Классика в прохладную погоду!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Мероприятие+прохладно',
        'clothes': 'Пиджак, водолазка, брюки, ботинки',
        'accessories': 'Платок, наручные часы'
    },
    'event_тепло': {
        'name': 'Элегантный летний лук',
        'description': 'Льняная рубашка, брюки-чинос, лоферы. Идеально для мероприятий в тепло!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Летнее+мероприятие',
        'clothes': 'Льняная рубашка, брюки-чинос, лоферы',
        'accessories': 'Солнцезащитные очки, часы'
    },

    'work_снег': {
        'name': 'Офисный лук в снег',
        'description': 'Шерстяной пиджак, рубашка, водолазка, брюки, ботинки. Тепло и строго!',
        'image': 'https://via.placeholder.com/400x300/45B7D1/FFFFFF?text=Офис+снег',
        'clothes': 'Пиджак, рубашка, водолазка, брюки, ботинки',
        'accessories': 'Шарф, кожаный портфель'
    },
    'work_дождь': {
        'name': 'Офис в дождливый день',
        'description': 'Тренч, рубашка-поло, брюки, кожаные туфли. Сухо и профессионально!',
        'image': 'https://via.placeholder.com/400x300/4ECDC4/FFFFFF?text=Офис+дождь',
        'clothes': 'Тренч, рубашка-поло, брюки, туфли',
        'accessories': 'Зонт, портфель'
    },
    'work_прохладно': {
        'name': 'Офисный стиль в прохладу',
        'description': 'Классическая рубашка, брюки-слим, дерби. Всегда актуально!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Офис+прохладно',
        'clothes': 'Рубашка, брюки, дерби',
        'accessories': 'Галстук, запонки'
    },
    'work_тепло': {
        'name': 'Летний офисный лук',
        'description': 'Легкая рубашка-поло, брюки-чинос, мокасины. Строго и не жарко!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Офис+тепло',
        'clothes': 'Рубашка-поло, брюки-чинос, мокасины',
        'accessories': 'Наручные часы, кожаный портфель'
    },

    'sport_снег': {
        'name': 'Зимняя экипировка',
        'description': 'Термобелье, флисовая кофта, спортивные штаны, зимние кроссовки. Для активного снега!',
        'image': 'https://via.placeholder.com/400x300/45B7D1/FFFFFF?text=Спорт+снег',
        'clothes': 'Термобелье, флис, штаны, кроссовки',
        'accessories': 'Шапка, перчатки, термос'
    },
    'sport_дождь': {
        'name': 'Спорт в дождливую погоду',
        'description': 'Водонепроницаемая куртка, лосины/штаны, кроссовки с мембраной. Не промокнешь!',
        'image': 'https://via.placeholder.com/400x300/4ECDC4/FFFFFF?text=Спорт+дождь',
        'clothes': 'Неопреновая куртка, лосины, кроссовки',
        'accessories': 'Кепка, спортивные часы'
    },
    'sport_прохладно': {
        'name': 'Спорт в прохладную погоду',
        'description': 'Лонгслив, спортивные штаны, кроссовки. Идеально для бега или фитнеса!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Спорт+прохладно',
        'clothes': 'Лонгслив, штаны, кроссовки',
        'accessories': 'Браслет-фитнес, бутылка'
    },
    'sport_тепло': {
        'name': 'Летняя спортивная форма',
        'description': 'Шорты-бегунки, футболка-поло, кроссовки. Легкость и комфорт в теплую погоду!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Спорт+тепло',
        'clothes': 'Шорты, футболка, кроссовки',
        'accessories': 'Спортивные часы, бутылка'
    },

    'beach_снег': {
        'name': 'Пляж в снег? Ты серьезно?',
        'description': 'Термобелье, кофта, джинсы, пуховик. Для самых смелых!',
        'image': 'https://via.placeholder.com/400x300/45B7D1/FFFFFF?text=Пляж+снег',
        'clothes': 'Термобелье, кофта, джинсы, пуховик',
        'accessories': 'Шапка, перчатки, термос'
    },
    'beach_дождь': {
        'name': 'Пляж в дождь?',
        'description': 'Непромокаемая куртка, шорты, резиновые сапоги. Дождь не помеха!',
        'image': 'https://via.placeholder.com/400x300/4ECDC4/FFFFFF?text=Пляж+дождь',
        'clothes': 'Куртка, шорты, сапоги',
        'accessories': 'Зонт, кепка'
    },
    'beach_прохладно': {
        'name': 'Пляж в прохладный день',
        'description': 'Легкая ветровка, шорты, кеды. Для прохладного дня у моря!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Пляж+прохладно',
        'clothes': 'Ветровка, шорты, кеды',
        'accessories': 'Солнечные очки, рюкзак'
    },
    'beach_тепло': {
        'name': 'Пляжный образ',
        'description': 'Плавки/купальник, парео, сланцы. Наслаждайся солнцем!',
        'image': 'https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Пляж+тепло',
        'clothes': 'Плавки/купальник, парео, сланцы',
        'accessories': 'Солнцезащитный крем, очки, шляпа'
    }
}

def get_weather(city_name):
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }

        response = requests.get(OPENWEATHER_URL, params=params, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'main_weather': data['weather'][0]['main'],
                'city': data['name'],
                'country': data['sys']['country'],
                'icon': data['weather'][0]['icon']
            }
        else:
            flash('Город не найден! Проверьте название (например: Москва, Лондон)', 'danger')
            return None

    except Exception as e:
        flash('Ошибка подключения к серверу погоды', 'danger')
        return None


def get_weather_category(weather_main, temp):
    if weather_main in ['Snow', 'Sleet']:
        return 'снег'
    elif weather_main in ['Rain', 'Drizzle', 'Thunderstorm']:
        return 'дождь'
    elif temp < 15:
        return 'прохладно'
    else:
        return 'тепло'


def get_outfit_key(event_type, weather_category):
    event_map = {
        'Прогулка': 'walk',
        'Мероприятие': 'event',
        'Работа': 'work',
        'Спорт': 'sport',
        'Пляж': 'beach'
    }

    event_key = event_map.get(event_type, 'walk')
    return f"{event_key}_{weather_category}"


def get_outfit(city_name, event_type):
    weather_data = get_weather(city_name)

    if not weather_data:
        return None, None

    weather_category = get_weather_category(
        weather_data['main_weather'],
        weather_data['temperature']
    )

    outfit_key = get_outfit_key(event_type, weather_category)
    outfit = OUTFITS_DATABASE.get(outfit_key)

    if not outfit:
        outfit = OUTFITS_DATABASE.get(f'walk_{weather_category}')

    weather_data['weather_category'] = weather_category

    weather_emoji = {
        'снег': '❄️',
        'дождь': '🌧',
        'прохладно': '⛅',
        'тепло': '☀️'
    }
    weather_data['category_emoji'] = weather_emoji.get(weather_category, '🌤')

    return outfit, weather_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        event = request.form.get('event', '')

        if not city:
            flash('Введите название города!', 'warning')
            return render_template('index.html')

        if not event:
            flash('Выберите мероприятие!', 'warning')
            return render_template('index.html')

        outfit, weather = get_outfit(city, event)

        if outfit and weather:
            session['outfit'] = outfit
            session['weather'] = weather
            session['city'] = city
            session['event'] = event

            flash(f'Отличный выбор для {city}! Смотри, что мы подобрали ', 'success')
            return redirect(url_for('result'))
        else:
            flash('Что-то пошло не так. Попробуйте еще раз!', 'danger')

    return render_template('index.html')


@app.route('/result')
def result():
    outfit = session.get('outfit')
    weather = session.get('weather')
    city = session.get('city')
    event = session.get('event')

    if not outfit or not weather:
        flash('Сначала подберите образ!', 'warning')
        return redirect(url_for('index'))

    return render_template('result.html',
                           outfit=outfit,
                           weather=weather,
                           city=city,
                           event=event)


@app.route('/reset')
def reset():
    session.clear()
    flash('Все сброшено! Можете подобрать новый образ', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)