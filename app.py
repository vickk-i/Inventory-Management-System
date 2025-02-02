from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import pymysql
from config import DB_CONFIG, SECRET_KEY
app = Flask(__name__)
app.secret_key = SECRET_KEY
bcrypt = Bcrypt(app)
# Database connection function
def get_db_connection():
    return pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
        conn.close()
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')
# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = get_db_connection()
        with conn.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                conn.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except:
                flash('Username already exists. Please choose a different one.', 'danger')
        conn.close()
    return render_template('register.html')
# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# Dashboard (Inventory list)
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)

# Add item
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO items (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
            conn.commit()
        conn.close()
        flash('Item added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_item.html')

# Update item
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        with conn.cursor() as cursor:
            cursor.execute("UPDATE items SET name = %s, quantity = %s, price = %s WHERE id = %s", (name, quantity, price, id))
            conn.commit()
        conn.close()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('index'))
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM items WHERE id = %s", (id,))
        item = cursor.fetchone()
    conn.close()
    return render_template('update_item.html', item=item)

# Delete item
@app.route('/delete/<int:id>')
def delete_item(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM items WHERE id = %s", (id,))
        conn.commit()
    conn.close()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
