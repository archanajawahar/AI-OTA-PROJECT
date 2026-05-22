from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "travelsecret"

from urllib.parse import urlparse

url = urlparse("mysql://root:rtNlpcRYhHkHktuZgNGqGUsOIMSvpzep@kodama.proxy.rlwy.net:20307/railway")

app.config['MYSQL_HOST'] = url.hostname
app.config['MYSQL_USER'] = url.username
app.config['MYSQL_PASSWORD'] = url.password
app.config['MYSQL_DB'] = url.path[1:]
app.config['MYSQL_PORT'] = url.port

mysql = MySQL(app)
with app.app_context():

    cursor = mysql.connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        password VARCHAR(100)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        destination VARCHAR(100)
    )
    """)

    mysql.connection.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cur.fetchone()

        cur.close()

        if user:
            name = user[1]
            session['user'] = name
            return render_template('dashboard.html', name=name)
        else:
            return render_template(
          'result.html',
           message="Invalid Email or Password"
           )

    return render_template('login.html')

    return render_template(
    'result.html',
    message="User Registered Successfully"
      )

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO users(name, email, password) VALUES(%s, %s, %s)",
            (name, email, password)
        )

        mysql.connection.commit()

        cur.close()

        session['user'] = name

        return redirect('/')

    return render_template('register.html')

@app.route('/book', methods=['GET', 'POST'])
def book():

    if request.method == 'POST':

        name = request.form['name']
        destination = request.form['destination']

        cursor = mysql.connection.cursor()

        cursor.execute(
            "INSERT INTO bookings(name, destination) VALUES(%s, %s)",
            (name, destination)
        )

        mysql.connection.commit()

        cursor.close()

        return render_template(
            'result.html',
            message="Ticket Booked Successfully"
        )

    return render_template('booking.html')
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():

    recommendation = ""

    if request.method == 'POST':

        place_type = request.form['category'].strip().lower()

        if place_type == "beach":

            recommendation = "Goa, Maldives, Bali, Pondicherry"

        elif place_type == "mountain":

            recommendation = "Ooty, Manali, Shimla, Munnar"

        elif place_type == "city":

            recommendation = "Chennai, Bangalore, Mumbai, Delhi"

        elif place_type == "adventure":

            recommendation = "Rishikesh, Ladakh, Dubai Safari"

        elif place_type == "nature":

            recommendation = "Kerala, Coorg, Alleppey"

        elif place_type == "vacation":

            recommendation = "Paris, Switzerland, Maldives"

        elif place_type == "spiritual":

            recommendation = "Varanasi, Tirupati, Kedarnath"

        elif place_type == "historical":

            recommendation = "Agra, Jaipur, Hampi"

        elif place_type == "wildlife":

            recommendation = "Jim Corbett, Bandipur, Kaziranga"

        elif place_type == "desert":

            recommendation = "Rajasthan, Dubai, Sahara"

        elif place_type == "island":

            recommendation = "Andaman, Lakshadweep, Bali"

        elif place_type == "snow":

            recommendation = "Kashmir, Switzerland, Himachal"

        elif place_type == "shopping":

            recommendation = "Dubai Mall, Singapore, Bangkok"

        elif place_type == "luxury":

            recommendation = "Dubai, Monaco, Maldives"

        elif place_type == "food":

            recommendation = "Italy, Chennai, Hyderabad"

        else:

            recommendation = "No Recommendation Available"

        return render_template(
            'result.html',
            message=f"Recommended Place: {recommendation}"
        )

    return render_template('recommendation.html')
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')
@app.route('/dashboard')
def dashboard():

    if 'user' in session:

        return render_template(
            'dashboard.html',
            name=session['user']
        )

    return redirect('/login')
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":

            cursor = mysql.connection.cursor()

            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

            cursor.execute("SELECT * FROM bookings")
            bookings = cursor.fetchall()

            return render_template(
                'admin_dashboard.html',
                users=users,
                bookings=bookings
            )

        else:

            return render_template(
                'result.html',
                message="Invalid Admin Credentials"
            )

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)