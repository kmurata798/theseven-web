import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# create table query 
CREATE_CUSTOMER_EMAIL = (
    "CREATE TABLE IF NOT EXISTS emails (id SERIAL PRIMARY KEY, name TEXT);"
)

# insert data / return id query
INSERT_EMAIL_RETURN_ID = "INSERT INTO emails (name) VALUES (%s) RETURNING id;"

load_dotenv()

app = Flask(__name__)

# PostgreSQL DB connection
# app.config['SQLALCHEMY_DATABASE_URI']= os.getenv("POSTGRES_URL")
# db = SQLAlchemy(app)
url = os.getenv("POSTGRES_URL")
connection = psycopg2.connect(url)

# Dummy/fake shopping cart
cart = [
    {
        'item_count': '1',
        'items': [
            {
                'id': '1',
                'option': ['name'],
                'product': [
                    {
                        'id': '1',
                        'name': 'red_sticker',
                        'url': "#",
                        'has_default_option': False
                    }
                ],
                'unit_price': '5.00'
            }
        ],
        'item_quantity': '2'
    }
]
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/profile")
def profile(name="bento"):
    return render_template('profile.html', name=name)

# Shopping cart routes
@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route("/products")
def products(cart=cart):
    return render_template('products.html', cart=cart)

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.post("/contact/sent")
def receive_customer_email():
    # ! get a python dictionary of data the client sent !
    # client sends a string with a specific structure
    # request.get_json takes that string and turns it into a dictionary
    data = request.get_json()
    name = data["name"]
    # subject = data["subject"]
    # Connect to the DB
    # connection allows us to start the connection
    with connection:
        # cursor is object allows us to insert data into DB/iterate over rows that DB returns if we make a query to select data
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CUSTOMER_EMAIL)
            # insert email and subject into DB + return the ID to cursor
            cursor.execute(INSERT_EMAIL_RETURN_ID, (name,))
            # Retrieve the ID from the cursor
            # if there are multiple columns, must include specific index at end
            customer_email_id = cursor.fetchone()[0]
            # 201 status code at the end means "created"
    return {"id": customer_email_id, "message": f" {name} website contact."}, 201

# Test out api endpoints/routes with postman. Make sure choose POST, GET, etc.
# for json input/output, go to Body > Raw > JSON

# $ python server.py
if __name__ == "__main__":
    app.run(debug=True)