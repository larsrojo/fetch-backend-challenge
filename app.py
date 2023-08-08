from flask import Flask, request, jsonify
from datetime import datetime
from math import ceil
from uuid import uuid4

app = Flask(__name__)

receipts = {}

def calculate_points(receipt_data):
    
    points = 0
    
    points += sum(c.isalnum() for c in receipt_data['retailer'])

    purchase_datetime = datetime.strptime(
        receipt_data['purchaseDate'] + ' ' + receipt_data['purchaseTime'],
        '%Y-%m-%d %H:%M'
    )
    
    if purchase_datetime.day % 2 != 0:
        points += 6
    
    if 14 <= purchase_datetime.hour < 16:
        points += 10

    total = float(receipt_data['total'])

    if total == round(total):
        points += 50
    
    if total % 0.25 == 0:
        points += 25
    
    num_items = len(receipt_data['items'])
    points += (num_items // 2) * 5

    for item in receipt_data['items']:
        trimmed_length = len(item['shortDescription'].strip())
        if trimmed_length % 3 == 0:
            item_price = float(item['price'])
            points += ceil(item_price * 0.2)
    
    return points

@app.route('/receipts/process', methods=['POST'])
def process_receipt():

    receipt_data = request.get_json()
    total_points = calculate_points(receipt_data)
    
    receipt_id = str(uuid4())
    receipts[receipt_id] = total_points

    response = {'id': receipt_id}

    return jsonify(response)

@app.route('/receipts/<string:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    
    if receipt_id in receipts:
        total_points = receipts[receipt_id]
        response = {'points': total_points}
    else:
        response = {'error': 'Receipt ID not found'}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5001
    )
