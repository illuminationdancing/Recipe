import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Hardcoded API credentials for testing purposes
APP_ID = 'dde6daa4'
APP_KEY = '009a9a1781b7e3e669a08caeb948525f'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/submit', methods=['POST'])
def submit():
    ingredient = request.form['ingredient']
    eating_in = request.form['dinner_plans']  # Get the value for the eating in question

    # Check if the user is eating in
    if eating_in.lower() != 'y':
        message = "You indicated that you're not eating in tonight."
        return render_template('home.html', message=message)

    # Edamam API call with the user-provided ingredient
    url = 'https://api.edamam.com/search'
    params = {
        'q': ingredient,
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'from': 0,
        'to': 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Check if any recipes are returned
    recipes = []
    if 'hits' in data and len(data['hits']) > 0:
        for hit in data['hits']:
            recipe = hit['recipe']
            is_vegan = 'Vegan' in recipe['healthLabels']
            recipes.append({
                "name": recipe['label'],
                "image": recipe['image'],
                "ingredients": recipe['ingredientLines'],
                "carbs_per_serving": round(recipe['totalNutrients']['CHOCDF']['quantity'] / recipe['yield'], 2),
                "vegan": is_vegan,
                "url": recipe['url']
            })

    return render_template('home.html', recipes=recipes)


if __name__ == '__main__':
    app.run(debug=True)
