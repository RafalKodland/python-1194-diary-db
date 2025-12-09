# Importowanie
from flask import Flask, render_template, request, redirect, session
# Podłączanie biblioteki do baz danych
from flask_sqlalchemy import SQLAlchemy

email = "mail użytkownika"

app = Flask(__name__)
# Ustawianie tajnego klucza dla sesji
app.secret_key = 'my_top_secret_123'
# Nawiązanie połączenia SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Tworzenie BD
db = SQLAlchemy(app)
# Tworzenie tabeli

class Card(db.Model):
    # Ustanowienie pól wejściowych
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Tytuł
    title = db.Column(db.String(100), nullable=False)
    # Podtytuł
    subtitle = db.Column(db.String(300), nullable=False)
    # Tekst
    text = db.Column(db.Text, nullable=False)
    # Adres e-mail właściciela karty
    user_email = db.Column(db.String(100), nullable=False)

    # Wyświetlanie obiektu i jego identyfikatora
    def __repr__(self):
        return f'<Card {self.id}>'
    

# Zadanie #1. Stwórz tabelę użytkowników (User)
class User(db.Model):
   # Tworzenie kolumn
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'

# Uruchamianie strony z treścią
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
            
        # Zadanie #4. Zaimplementuj weryfikację użytkownika
        users_db = User.query.all()

        for user in users_db:
            if form_login == user.mail and form_password == user.password:
                session['user_email'] = user.mail
                return redirect('/index')

        error = 'Niepoprawny login lub hasło'
        return render_template('login.html', error=error)
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Zadanie #3. Wdrożenie rejestrowania użytkowników
        new_user = User(mail=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


# Uruchamianie strony z treścią
@app.route('/index')
def index():
    # Zadanie #4. Upewnij się, że użytkownik widzi tylko swoje karty.
    email = session.get('user_email')
    cards = Card.query.filter_by(user_email=email).all()
    return render_template('index.html', cards=cards)

# Uruchomienie strony z kartami
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Uruchomienie strony tworzenia karty
@app.route('/create')
def create():
    return render_template('create_card.html')

# Formularz karty
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Zadanie #4. Twórz karty w imieniu użytkownika
        email = session['user_email']
        card = Card(title=title, subtitle=subtitle, text=text, user_email=email)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
