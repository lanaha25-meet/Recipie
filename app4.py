from flask import Flask, redirect, render_template, request, url_for ,flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyA4nrA8ELS1ohcg0iBbgCQdfSfzO7sJSyU",
  "authDomain": "food-1e9da.firebaseapp.com",
  "projectId": "food-1e9da",
  "storageBucket": "food-1e9da.appspot.com",
  "messagingSenderId": "1073017476935",
  "appId": "1:1073017476935:web:c660a75bbfdd7a0ae0de62",
  "measurementId": "G-CFT0YYT69X",
  "databaseURL":"https://food-1e9da-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app=Flask(__name__, template_folder='templates', static_folder="static")

app.config['SECRET_KEY'] = "rotemisawesome"

@app.route('/home')
def home():
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_ref = db.child('users')
        users = user_ref.get()

        if users and email in users and users[email]['password'] == password:
            session['user'] = email
            return redirect(url_for('ingredients'))
    else:   # else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        

        try :
            login_session['users']=auth.creat_user_with_email_and_password(email,password)
            user_id=login_session['users']['localId']
            user_ref = db.child('users').set({
            "email": email,
            "password": password
            })
        except:
            # user_ref.child(email).set({'password': password})
            # flash('Account created successfully')
            # return redirect(url_for('login'))
            flash('Email already exists')
        return redirect(url_for("ingredients"))
    else:
        return render_template('signup.html')

@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    if request.method == 'POST':
        ingredients=request.form['ingredient']
        return redirect(url_for('recipes', ingredients=ingredients))
    else:
        return render_template("ingredients.html")
    

@app.route('/recipes')
def recipes():
    try: 
        ingredients = login_session.get('ingredients', [])
        recipes_ref = db.child('recipes').push({
            "ingredients":ingredients,
            })
        all_recipes = db.child('recipes').get()
        if not recipes_ref.each():
            return render_template('recipes.html', recipes=[])

        all_recipes = recipes_ref.val()
        matching_recipes = [
            recipe for recipe in all_recipes.values()
            if set(ingredients).issubset(set(recipe.get('ingredients', [])))
        ]
        return render_template('recipes.html', recipes=matching_recipes)
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('error.html', message=str(e))

if __name__ == '__main__':
    app.run(debug=True)







