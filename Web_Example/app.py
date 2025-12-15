from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "product_data.json"

# If data file doesn't exist, create default product
if not os.path.exists(DATA_FILE):
    product = {
        "title": "UltraVision 55\" 4K Smart TV",
        "description": "Crystal-clear 4K display with HDR10, WiFi connectivity, and built-in streaming apps.",
        "price": 499.99,
        "image": "/static/images/tv.jpg"
    }
    with open(DATA_FILE, "w") as f:
        json.dump(product, f, indent=4)

def load_product():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_product(product):
    with open(DATA_FILE, "w") as f:
        json.dump(product, f, indent=4)

@app.route("/")
def product_page():
    product = load_product()
    return render_template("product.html", product=product)

@app.route("/update_price/<float:new_price>")
def update_price(new_price):
    product = load_product()
    product["price"] = new_price
    save_product(product)
    return jsonify({"message": "Price updated", "new_price": new_price})

if __name__ == "__main__":
    app.run(debug=True)
