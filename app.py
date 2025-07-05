from flask import Flask, redirect, render_template, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'tajny_klucz'

USERS = {
    'arek11' : 'qwerty'
}

produkty = {
    'produkt_1': {'nazwa': 'WODA', 'cena': 3},
    'produkt_2': {'nazwa': 'MIÓD', 'cena': 50},
    'produkt_3': {'nazwa': 'PIWO', 'cena': 5},
    'produkt_4': {'nazwa': 'CHLEB', 'cena': 4},
    'produkt_5': {'nazwa': 'JAJKO', 'cena': 2},
    'produkt_6': {'nazwa': 'MASŁO', 'cena': 8}
}

class Formularz(FlaskForm):
    login = StringField('LOGIN', validators=[DataRequired(message='Należy podać login')])
    haslo = PasswordField("HASŁO", validators=[DataRequired(message='Należy podać hasło')])
    zatwierdz = SubmitField('Zatwierdź')

@app.route('/login', methods=['POST','GET'])
def login():
    form = Formularz()
    if form.validate_on_submit():
        login = form.login.data
        haslo = form.haslo.data
        if login in USERS and USERS[login] == haslo:
            session['user'] = login
            flash('Zalogowano poprawnie')
            return redirect(url_for('home'))
        else:
            flash('Niepoprawny login lub hasło')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/home')
def home():
    if not session.get('user'):
        flash('Należy się zalogować')
        return redirect(url_for('login'))
    return render_template('home.html', produkty=produkty, user=session.get('user'))

@app.route('/logout')
def logout():
    if not session.get('user'):
        flash('Należy się zalogować')
        return redirect(url_for('login'))
    session.pop('user')
    flash('Wylogowano poprawnie')
    return redirect('login')

@app.route('/dodaj_do_koszyka/<string:id_produktu>')
def dodaj_do_koszyka(id_produktu):
    if not session.get('user'):
        flash('Należy się zalogować')
        return redirect(url_for('login'))
    koszyk = session.get('koszyk', {})
    if id_produktu not in koszyk:
        koszyk[id_produktu] = 0
    koszyk[id_produktu] += 1
    session['koszyk'] = koszyk
    flash(f'Dodano produkt {produkty[id_produktu]["nazwa"]} do koszyka')
    return redirect(url_for('home'))

@app.route('/koszyk')
def koszyk():
    if not session.get('user'):
        flash('Należy się zalogować')
        return redirect(url_for('login'))
        
    koszyk = session.get('koszyk', {})
    suma = 0
    zawartosc = []
    
    for id_produktu, ilosc in koszyk.items():
        zawartosc.append({
        'nazwa' : produkty[id_produktu]['nazwa'],
        'cena' : produkty[id_produktu]['cena'],
        'ilosc' : ilosc,
        'cena_razy_ilosc' : produkty[id_produktu]['cena'] * ilosc
        })
        suma += produkty[id_produktu]['cena'] * ilosc
    return render_template('koszyk.html', suma=suma, zawartosc=zawartosc)

@app.route('/wyczysc_koszyk')
def wyczysc_koszyk():
    if not session.get('user'):
        flash('Należy się zalogować')
        return redirect(url_for('login'))
    session['koszyk'] = {}
    flash('Koszyk wyczyszczono')
    return redirect(url_for('koszyk'))

if __name__ == '__main__':
    app.run(debug=True)