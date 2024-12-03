from ticket import app, db
from flask import render_template, request, url_for, redirect, flash, make_response
from sqlalchemy import text

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/bestellungen')
def bestellungen_page():
    username = request.cookies.get('username')
    if not username:
        flash("Bitte loggen Sie sich ein, um die Bestellungen einzusehen.", category='warning')
        return redirect(url_for('login_page'))
    
    print("Username aus Cookie: ", username)
    
    query_stmt = "SELECT * FROM bestellungen WHERE username = :username"
    result = db.session.execute(text(query_stmt), {'username': username})
    orders = result.fetchall()

    return render_template('bestellungen.html', orders=orders)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        query_stmt = text(f"SELECT username FROM testusers WHERE username = '{username}' AND password = '{password}'")
        result = db.session.execute(query_stmt)
        user = result.fetchone()

        if not user:
            flash("Login fehlgeschlagen. Versuchen Sie es erneut.", category='warning')
            return render_template('login.html')

        response = make_response(redirect(url_for('bestellungen_page')))
        response.set_cookie('username', user[0], httponly=False)  # 'httponly=False' macht es für JS zugänglich
        
        print("Cookie gesetzt für Benutzer:", user[0])
        
        return response

    return render_template('login.html')


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home_page')))
    response.delete_cookie('username')  # Löscht das Cookie
    return response

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        insert_stmt = "INSERT INTO testusers (username, password) VALUES (:username, :password)"
        db.session.execute(text(insert_stmt), {'username': username, 'password': password})
        db.session.commit()
        
        flash("Registrierung erfolgreich! Bitte melden Sie sich an.", category='success')
        return redirect(url_for('login_page'))

    return render_template('register.html')

@app.route('/pizza_bestellen', methods=['GET', 'POST'])
def pizza_bestellen():
    username = request.cookies.get('username')
    if not username:
        flash("Bitte loggen Sie sich ein, um eine Bestellung aufzugeben.", category='warning')
        return redirect(url_for('login_page'))

    return render_template('pizzabestellung.html')

@app.route('/pizza_bestellt', methods=['POST'])
def pizza_bestellt():
    username = request.cookies.get('username')
    if not username:
        flash("Bitte loggen Sie sich ein, um eine Bestellung aufzugeben.", category='warning')
        return redirect(url_for('login_page'))
    
    print("Benutzername im Cookie:", username) 

    order = {
        'Margherita': int(request.form.get('margherita_quantity', 0)),
        'Salami': int(request.form.get('salami_quantity', 0)),
        'Hawaii': int(request.form.get('hawaii_quantity', 0)),
        'Veggie': int(request.form.get('veggie_quantity', 0))
    }

    custom_pizza_name = request.form.get('custom_pizza', '').strip()
    custom_pizza_quantity = int(request.form.get('custom_pizza_quantity', 0))
    if custom_pizza_name and custom_pizza_quantity > 0:
        order[custom_pizza_name] = custom_pizza_quantity

    print("Bestellparameter:", order)  # Gibt die Bestellparameter aus

    for pizza, quantity in order.items():
        if quantity > 0:
            insert_stmt = """
            INSERT INTO bestellungen (username, pizza_type, quantity)
            VALUES (:username, :pizza_type, :quantity)
            """
            db.session.execute(
                text(insert_stmt),
                {'username': username, 'pizza_type': pizza, 'quantity': quantity}
            )
    
    db.session.commit()
    
    flash("Ihre Bestellung wurde erfolgreich aufgegeben!", category='success')
    return redirect(url_for('bestellungen_page'))

@app.route('/bestellungen_anzeigen')
def bestellungen_anzeigen():
    username = request.cookies.get('username')
    if not username:
        flash("Bitte loggen Sie sich ein, um Ihre Bestellungen einzusehen.", category='warning')
        return redirect(url_for('login_page'))

    query_stmt = "SELECT * FROM bestellungen WHERE username = :username"
    result = db.session.execute(text(query_stmt), {'username': username})
    orders = result.fetchall()
    print(orders)
    return render_template('bestellungen.html', orders=orders)
