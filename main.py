import requests
import os  # To access environment variables

from flask import Flask, render_template, request

app = Flask(__name__)

# Access the API credentials securely from environment variables
APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/submit', methods=['POST'])
def submit():
    ingredient = request.form['ingredient']

    # Edamam API call with the user-provided ingredient
    url = 'https://api.edamam.com/search'
    params = {
        'q': ingredient,
        'app_id': APP_ID,  # Use the environment variable
        'app_key': APP_KEY,  # Use the environment variable
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
            is_vegan = 'Vegan' in recipe['healthLabels']  # Check for vegan label
            recipes.append({
                "name": recipe['label'],
                "image": recipe['image'],  # Extract the image link
                "ingredients": recipe['ingredientLines'],
                "carbs_per_serving": round(recipe['totalNutrients']['CHOCDF']['quantity'] / recipe['yield'], 2),
                "vegan": is_vegan,
                "url": recipe['url']
            })

    # Pass the recipes to the HTML template for display
    return render_template('home.html', recipes=recipes)


if __name__ == '__main__':
    app.run(debug=True)
