import boto3
import uuid
from flask import Flask, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import check_user
import logging
# Flask Setup
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
bcrypt = Bcrypt(app)
CORS(app)

# AWS DynamoDB Client
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")  # Replace with your AWS region
users_table = dynamodb.Table("owuser")

# Helper: Check if user exists
def get_user(email):
    response = users_table.get_item(Key={"email": email})
    return response.get("Item")

# Login Endpoint
@app.route("/login", methods=["POST"])
def login():
    print(request)
    data = request.json
    print(data)
    app.logger.info(data)
    username = data["username"]
    password = data["password"]
    code= data["code"]
    user = check_user.check_user(username, password, code)
    app.logger.info(user)
    if not user: 
        return jsonify({"error": "Invalid login credentials"}), 401
    else:
        return jsonify({"message": "Login successful!", "user_id": username}), 200

# Serve HTML Form
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
#    app.run(debug=True,port=5000)
    app.run(debug=True,host='0.0.0.0',port=5000)
