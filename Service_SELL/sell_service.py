from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/sell
'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/sell', methods=['POST'])
def sell_product():
    data = request.get_json()
    s = Sale(product=data['product'], quantity=data['quantity'], price=data['price'])
    db.session.add(s)
    db.session.commit()

    # Generate CSV invoice
    filename = f"sell_invoice_{s.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Product', 'Quantity', 'Price'])
        writer.writerow([s.id, s.product, s.quantity, s.price])

    return jsonify({'message': 'Sale recorded', 'invoice': filename})

if __name__ == '__main__':
    app.run(port=8003, debug=True)
