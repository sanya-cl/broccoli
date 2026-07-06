from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

RECIPES = {
    'Омлет': ['яйца', 'молоко', 'масло'],
    'Бутерброд с сыром': ['хлеб', 'масло', 'сыр'],
    'Бутерброд с колбасой': ['хлеб', 'масло', 'колбаса'],
    'Салат из помидоров и огурцов': ['помидор', 'огурец'],
    'Курица с рисом': ['курица', 'рис', 'лук', 'морковь'],
    'Гречка с курицей': ['гречка', 'курица', 'лук', 'морковь'],
    'Макароны с сыром': ['макароны', 'сыр', 'масло'],
    'Картофель с курицей': ['картофель', 'курица', 'лук', 'морковь'],
    'Котлеты на пару':['курица', 'рис'],
    'Котлеты из говядины':['говядина', 'манная крупа', 'лук']

}
DIET_PLANS = [
    {
        'id': 1,
        'name': 'Здоровое питание',
        'for_whom':'Для тех, кто хочет сбалансированное питание',
        'principles': ['3 приема пищи + 2 перекуса', 'БЖУ 30/20/50', 'пить воду +-2 литра в день', 'Исключить фастфуд, сладкие газировки'],
        'menu': {
            "Завтрак": 'Каша + Бутерброд с сыром + чай',
            "Перекус 1": 'Яблоко/банан',
            'Обед': 'Суп с лапшой + Салат из овощей',
            'Перекус 2': 'Творог/йогурт',
            'Ужин': 'Рыба на пару' + 'Овощи'
        }
    },
    {
        'id': 2,
        'name': 'Диета №1',
        'for_whom': 'Заболевания ЖКТ',
        'principles': ['5 маленьких приемов пищи', 'измельчать всю еду', 'исключить кислое, острое, жаренное',
                       'исключить грубую клетчатку'],
        'menu': {
            "Завтрак": 'Омлет + чай',
            "Перекус 1": 'Сухарики + кисель',
            'Обед': 'Суп-пюре овощной + рисовая каша',
            'Перекус 2': 'Творог/йогурт',
            'Ужин': 'Котлета на пару + картофельное пюре'
        }
    },
    {
        'id': 3,
        'name': 'Диета №5',
        'for_whom': 'Для печени',
        'principles': ['ограниченные жиры', 'исключить жареное, капченое, соленое', 'больше белков',
                       'есть овощи и фрукты'],
        'menu': {
            "Завтрак": 'Творог + каша + чай',
            "Перекус 1": 'Печеное яблоко',
            'Обед': 'Суп овощной + курица на пару с гречкой',
            'Перекус 2': 'Кефир с сухариками',
            'Ужин': 'Рыба на пару' + 'Овощи'
        }
    },
]

def get_diet_plan(available_products):


    available = set(p.lower().strip() for p in available_products if p.strip())
    dishes = []
    missing = {}
    for dish, ingredients in RECIPES.items():
        need = set(i.lower() for i in ingredients)
        if need.issubset(available):
            dishes.append(dish)
        else:
            miss = list(need - available)
            if miss:
                missing[dish] = miss
    return dishes, missing

def calculate_bmi(weight, height):
    if height <= 0 or weight <= 0:
        return None
    height_m = height / 100.0
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def bmi_category(bmi):
    if bmi < 18.5: return 'Недостаточный вес'
    elif bmi < 25: return 'Нормальный вес'
    elif bmi < 30: return 'Избыточный вес'
    else: return 'Ожирение'


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        name = request.form.get('user_name', '').strip()
        if name:
            session['user_name'] = name
        raw_products = request.form.get('products', '')

        products = [p.strip() for p in raw_products.split(',') if p.strip()]
        if not products:
            return render_template('index.html', error='Введите хотя бы один продукт!')


        dishes, missing = get_diet_plan(products)


        session['last_products'] = raw_products


        return render_template('index.html',
                               products=products,
                               dishes=dishes,
                               missing=missing,
                               user_name=session.get('user_name', ''))


    user_name = session.get('user_name', '')
    last_products = session.get('last_products', '')
    return render_template('index.html', user_name=user_name, last_products=last_products)

@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    result = None
    if request.method == 'POST':

        name = request.form.get('name', '').strip()
        if not name:
            name = session.get('user_name', '')
        if name:
            session['user_name'] = name

        try:
            weight = float(request.form.get('weight', 0))
            height = float(request.form.get('height', 0))
        except ValueError:
            weight = height = 0

        bmi_val = calculate_bmi(weight, height)
        if bmi_val is not None:
            category = bmi_category(bmi_val)
            result = {
                'name': name,
                'weight': weight,
                'height': height,
                'bmi': bmi_val,
                'category': category
            }
        else:
            result = {'error': 'Введите корректные рост и вес (положительные числа)'}

    user_name = session.get('user_name', '')
    return render_template('bmi.html', result=result, user_name=user_name)

@app.route('/diets', methods=['GET', 'POST'])
def diets():
    if request.method == 'POST':
        selected_index = request.form.get('diet_select', type=int)
        if selected_index is not None:
            session['diet_index'] = selected_index
            return redirect(url_for('diets'))
    current_index = session.get('diet_index', 0)
    if current_index < 0:
        current_index = len(DIET_PLANS) - 1
    elif current_index >= len(DIET_PLANS):
        current_index = 0
    diet = DIET_PLANS[current_index]
    return render_template('diets.html', diet=diet, current_index=current_index, total=len(DIET_PLANS))



if __name__ == '__main__':
    app.run(debug=True)