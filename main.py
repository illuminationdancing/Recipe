from flask import Flask, request, render_template
import requests

app = Flask(__name__)


# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')


# Route for dinner plans and recipe suggestion
@app.route('/dinner', methods=['POST'])
def dinner():
    # Get dinner plans input from the user
    dinner_plans = request.form.get('dinner_plans')

    if dinner_plans.lower() == 'y':
        ingredient = request.form.get('ingredient')

        # Set up API credentials
        APP_ID = 'dde6daa4'
        APP_KEY = '009a9a1781b7e3e669a08caeb948525f'

        # Define the URL and parameters for the Edamam Recipe API
        url = 'https://api.edamam.com/search'
        params = {
            'q': ingredient,
            'app_id': APP_ID,
            'app_key': APP_KEY,
            'from': 0,
            'to': 5  # Get up to 5 recipes
        }

        # Make a request to the API
        response = requests.get(url, params=params)
        data = response.json()

        # Check if recipes were returned
        recipes = []
        if 'hits' in data and len(data['hits']) > 0:
            for hit in data['hits']:
                recipe = hit['recipe']
                is_vegan = 'Vegan' in recipe['healthLabels']

                recipes.append({
                    "name": recipe['label'],
                    "ingredients": recipe['ingredientLines'],
                    "carbs_per_serving": round(recipe['totalNutrients']['CHOCDF']['quantity'] / recipe['yield'], 2),
                    "vegan": is_vegan,
                    "url": recipe['url'],
                    "image": recipe['image']  # Include the recipe image URL
                })
        else:
            recipes = None  # No recipes found

        # Pass recipes and a message back to the template
        return render_template('home.html', message="Here are some recipe suggestions!", recipes=recipes)
    else:
        # If not eating in
        return render_template('home.html', message="Enjoy your meal out!")


if __name__ == '__main__':
    app.run(debug=True)
