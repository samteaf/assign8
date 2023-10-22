from flask import Flask, request, jsonify 
import hashlib
import requests
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

#md5 Endpoint 
@app.route('/md5/<string:string>', methods=['GET'])
def md5_hash(string):
    md5_hash = hashlib.md5(string.encode()).hexdigest()
    return jsonify(input=string, output=md5_hash)

#Factorial Endpoint (Will break with very high numbers like "999999")   
@app.route('/factorial/<int:num>', methods=['GET'])
def factorial(num):
    if num < 0: 
        return jsonify(error="Input must be a non-negative integer") 
    
    result = 1 
    for i in range(1, num+ 1): 
        result *= i 
    
    return jsonify(input=num, output=result)


#Fibonacci Endpoint
@app.route('/fibonacci/<int:num>', methods=['GET'])
def fibonacci(num):
    if num < 0:
        return jsonify(error="Input must be a non-negative integer")

    fib_sequence = []
    a, b = 0, 1
    while a <= num:
        fib_sequence.append(a)
        a, b = b, a + b

    return jsonify(input=num, output=fib_sequence)

# Is prime Endpoint 
@app.route('/is-prime/<int:num>', methods=['GET'])
def is_prime(num):
    if num <= 1:
        return jsonify(input=num, is_prime=False, error="Input must be greater than 1")
    
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return jsonify(input=num, is_prime=False)
    
    return jsonify(input=num, is_prime=True)

# Slack Alert 

slack_WH_URL = "https://hooks.slack.com/services/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"

@app.route('/slack-alert/<string:message>', methods=['GET', 'POST'])
def slack_alert(message):
    #URL decode message
    decrypted_message = requests.utils.unquote(message)
    #make payload for json
    payload = {
        "text": decrypted_message,
        "username": "group8bot",
    }
    #send post request to slack
    try:
        response = requests.post(slack_WH_URL, json=payload)

        if response.status_code == 200:
            return jsonify({"success": True, "message": f"Message '{decrypted_message}' sent successfully to Slack."})
        
        else:
            return jsonify({"success": False, "message": "Failed to send message to Slack."}), 500
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/keyval', methods=['POST'])
def create_keyval():
    data = request.get_json()
    storage_key = data.get('storage-key')
    storage_val = data.get('storage-val')
    if redis_client.exists(storage_key):
        return jsonify({
            'storage-key': storage_key,
            'storage-val': storage_val,
            'command': f'CREATE {storage_key}/{storage_val}',
            'result': False,
            'error': 'Key already exists.'
        }), 409
    redis_client.set(storage_key, storage_val)
    return jsonify({
        'storage-key': storage_key,
        'storage-val': storage_val,
        'command': f'CREATE {storage_key}/{storage_val}',
        'result': True,
        'error': ''
    }), 200
@app.route('/keyval/<string>', methods=['GET'])
def read_keyval(string):
    storage_key = string
    storage_val = redis_client.get(storage_key)
    if storage_val is None:
        return jsonify({
            'storage-key': storage_key,
            'storage-val': '',
            'command': f'READ {storage_key}',
            'result': False,
            'error': 'Key does not exist.'
        }), 404
    return jsonify({
        'storage-key': storage_key,
        'storage-val': storage_val.decode('utf-8'),
        'command': f'READ {storage_key}',
        'result': True,
        'error': ''
    }), 200
@app.route('/keyval/<string:key>', methods=['PUT'])
def update_keyval(key):
    data = request.get_json()
    storage_val = data.get('storage-val')
    if redis_client.exists(key):
        redis_client.set(key, storage_val)
        return jsonify({
            'storage-key': key,
            'storage-val': storage_val,
            'command': f'UPDATE {key}/{storage_val}',
            'result': True,
            'error': ''
        }), 200
    else:
        return jsonify ({
            'storage-key': key,
            'storage-val': '',
            'command': f'UPDATE {key}/{storage_val}',
            'result': False,
            'error': 'Key does not exist.'
        }), 404

# Flask specify port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)