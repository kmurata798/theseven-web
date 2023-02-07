from flask import Flask, render_template

app = Flask(__name__)

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