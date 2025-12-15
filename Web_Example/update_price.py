from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = "product_data.json"

def load_product():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_product(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def product_page():
    product = load_product()
    return render_template("product.html", product=product)

# -------------------------
# UPDATE PRICE ENDPOINT
# -------------------------
@app.route("/update-price", methods=["POST"])
def update_price():
    data = request.json
    new_price = data.get("price")

    product = load_product()
    product["price"] = new_price
    save_product(product)

    return jsonify({"status": "success", "new_price": new_price})
    

if __name__ == "__main__":
    app.run(debug=True)



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!

import requests

requests.post(
    "http://127.0.0.1:5000/update-price",
    json={"price": 450.99}
)

################################