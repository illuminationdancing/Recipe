from flask import Flask, render_template, request

app = Flask(__name__)


# Route for the home page (form input)
@app.route('/')
def home():
    return render_template('home.html')


# Route to handle the form submission
@app.route('/submit', methods=['POST'])
def submit():
    age = request.form['age']
    gender = request.form['gender']
    state = request.form['state']

    return f'Hello, {age} year old {gender}! Nice to see you here. Nice to hear that you are {state}.'


if __name__ == '__main__':
    app.run(debug=True)
