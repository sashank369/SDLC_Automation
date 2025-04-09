from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = {
        'userId': 'sample_user_id',
        'message': 'User successfully registered'
    }
    return jsonify(response), 201

if __name__ == '__main__':
    app.run(debug=True)