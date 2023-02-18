import os
import psycopg2
import models

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

# PostgreSQL DB connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRES_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# url = os.getenv("POSTGRES_URL")
# connection = psycopg2.connect(url)
        
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

@app.route("/contact/sent", methods=['GET', 'POST'])
def submit_support():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # email_confirm = request.form['email_confirm']
        message = request.form['message']

        # Create supportTicket object from contact form
        support_ticket = models.SupportTicket(name, email, message)
        # open up session to the db and add ticket to the session
        db.session.add(support_ticket)
        # committing ticket to database
        db.session.commit()

    # if request.method == 'GET':
    # fetch a certain ticket
        ticketResult = db.session.query(models.SupportTicket).filter(models.SupportTicket.id == 1)
        for result in ticketResult:
            print(result.name)
    
    return redirect("/")

# Test out api endpoints/routes with postman. Make sure choose POST, GET, etc.
# for json input/output, go to Body > Raw > JSON

# $ python server.py
if __name__ == "__main__":
    app.run(debug=True)