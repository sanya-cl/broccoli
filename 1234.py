from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your secret key is here'

WEATHER_OUTFITS = {
    'sunny_hot': {
        'id': 1,
        'name': 'Жарко, без дождя, свободный стиль',
        'price': 4000,
        'description': 'Данный стиль одежды подойдет для прогулки с друзьями и развлечений на улице в жаркий летний и ясный день :-]',
        'category': 'Погулять, Свободный стиль',
        'image': 'https://usmall.ru/product/14055912-spidey-marvel-t-shirt-and-bermuda-jogging-set-zara',
        'main': 'Основные элементы одежды: Футболка, шорты, легкие кросовки',
        'accessories': 'Возможные акссессуары: Солнечные очки, кепка/панамка',
        'weather_condition': 'Жарко, солнечно',
        'event_type': 'Прогулка'
    },
    'rainy_cool': {
        'id': 2,
        'name': 'Не сильно холодно, грибной дождь/дождь средней силы, свободный стиль',
        'price': 8000,
        'description': 'Данный стиль одежды подойдет для прогулки и для того, чтобы добраться до нужного места в легкий дождь :-]',
        'category': 'В дождь',
        'image': 'https://pictures.pibig.info/27993-risunok-idet-dozhd.html',
        'main': 'Основные элементы одежды: Футболка, кофта, джинсы/штаны, кеды/непромокаемые сапоги',
        'accessories': 'Возможные акссессуары: Зонт',
        'weather_condition': 'Прохладно, дождливо',
        'event_type': 'Прогулка'
    },
    'hot_event': {
        'id': 3,
        'name': 'Жарко, но нужно на мероприятие',
        'price': 7000,
        'description': 'Когда в теплый или жаркий день нужно на мероприятие',
        'category': 'Тепло, мероприятие',
        'image': 'https://usmall.ru/product/6350628-solid-interlock-polo-shirt-us-polo-assn',
        'main': 'Основные элементы одежды: Футболка поло, легкие брюки/шорты',
        'accessories': 'Возможные акссессуары: часы, Солнечные очки',
        'weather_condition': 'Жарко',
        'event_type': 'Мероприятие'
    },
    'cold_winter': {
        'id': 4,
        'name': 'Холодно, зима или ранняя весна',
        'price': 20000,
        'description': 'В обычный зимний день можете использовать этот аутфит',
        'category': 'Зима, холодно',
        'image': 'https://albione.ru/blog/style/kak-odetsya-stilno-zimoy/?srsltid=AfmBOoqxbzfhB8gBaEAJJrje5E0mAlwwof6MBCuaUR6Ur3sY_jEnIb2b',
        'main': 'Основные элементы одежды: куртка, кофта, джинсы, подштаники, ботинки',
        'accessories': 'Возможные акссессуары: Шарф, шапка',
        'weather_condition': 'Холодно, зимой',
        'event_type': 'Прогулка'
    }
}


def get_outfit_by_id(outfit_id):
    for outfit in WEATHER_OUTFITS.values():
        if outfit['id'] == outfit_id:
            return outfit
    return None


def get_all_outfits():
    return list(WEATHER_OUTFITS.values())


def recommend_outfit(weather_condition, event_type):
    best_match = None
    for outfit in WEATHER_OUTFITS.values():
        if (weather_condition in outfit['weather_condition'] or
            outfit['weather_condition'] in weather_condition) and \
                (event_type in outfit['event_type'] or outfit['event_type'] in event_type):
            best_match = outfit
            break
    if best_match is None:
        for outfit in WEATHER_OUTFITS.values():
            if weather_condition in outfit['weather_condition'] or \
                    outfit['weather_condition'] in weather_condition:
                best_match = outfit
                break
    return best_match


@app.route('/', methods=['GET', 'POST'])
def index():
    recommended_outfits = []
    selected_date = None

    if request.method == 'POST':
        selected_date = request.form.get('date')
        weather_condition = request.form.get('weather')
        event_type = request.form.get('event')
        outfit_id = request.form.get('outfit_id')

        if outfit_id:
            outfit = get_outfit_by_id(int(outfit_id))
            if outfit:
                recommended_outfits = [outfit]
                flash(f'Выбран аутфит: {outfit["name"]}', 'success')
        elif weather_condition and event_type:
            outfit = recommend_outfit(weather_condition, event_type)
            if outfit:
                recommended_outfits = [outfit]
                flash(f'Рекомендованный аутфит: {outfit["name"]}', 'success')
            else:
                flash('Не найдено подходящего аутфита', 'warning')
        elif weather_condition:
            for outfit in WEATHER_OUTFITS.values():
                if weather_condition in outfit['weather_condition'] or \
                        outfit['weather_condition'] in weather_condition:
                    recommended_outfits.append(outfit)
            if recommended_outfits:
                flash('Найдены подходящие аутфиты по погоде', 'success')
            else:
                flash('Не найдено аутфитов для выбранной погоды', 'warning')
        else:
            flash('Пожалуйста, выберите погоду или конкретный аутфит', 'warning')

    return render_template('index.html',
                           outfits=get_all_outfits(),
                           recommended=recommended_outfits,
                           selected_date=selected_date)


@app.route('/outfit/<int:outfit_id>')
def outfit_detail(outfit_id):
    outfit = get_outfit_by_id(outfit_id)
    if outfit is None:
        flash('Аутфит не найден', 'danger')
        return redirect(url_for('index'))
    return render_template('outfit_detail.html', outfit=outfit)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)