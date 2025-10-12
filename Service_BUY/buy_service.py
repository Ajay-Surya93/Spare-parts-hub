from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://1234@localhost/buy'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/buy', methods=['POST'])
def buy_product():
    data = request.get_json()
    p = Purchase(product=data['product'], quantity=data['quantity'], price=data['price'])
    db.session.add(p)
    db.session.commit()

    # Generate CSV invoice
    filename = f"buy_invoice_{p.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Product', 'Quantity', 'Price'])
        writer.writerow([p.id, p.product, p.quantity, p.price])

    return jsonify({'message': 'Purchase recorded', 'invoice': filename})

if __name__ == '__main__':
    app.run(port=8002, debug=True)
