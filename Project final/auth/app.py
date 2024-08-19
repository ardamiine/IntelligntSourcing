from flask import Flask,jsonify,request,render_template,send_from_directory
from flask_jwt_extended import JWTManager,create_access_token,jwt_required

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = '123'
jwt = JWTManager(app)

users = {}

@app.route('/',methods=['POST','GET'])
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST','GET'])
def register():
    username = request.json.get['username']
    password = request.json.get['password']
    if username in users:
        return jsonify({"msg": "user already exists"})
    users[username] = password
    return jsonify[{"msg": "user already exists"}],201

@app.route('/login',methods=['POST'])
def login():
    pass

@app.route('/protected',methods=['GET'])
@jwt_required()
def protected():
    pass
if __name__ == '__main__':
    app.run(debug=True)