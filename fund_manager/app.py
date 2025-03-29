
from . import app,db
from flask import request, make_response, jsonify
from .models import Fund, User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps



@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    firstn = data.get("firstname")
    lastn = data.get("lastname")

    if firstn and lastn and email and password:
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return make_response({"message": "User already exists"}, 200)
            hasehdpassword = generate_password_hash(password)
            new_user = User(firstname=firstn, lastname=lastn, email=email, password=hasehdpassword)
            db.session.add(new_user)
            db.session.commit()
            return make_response({"message": "User created successfully"},201)
        except Exception as e:
            print(e)
            db.session.rollback()       
            return make_response({"message": "An error occurred"}, 500)
    else:
        return make_response({"message": "Invalid data"}, 400)
    




@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if email and password:
        user = User.query.filter_by(email=email).first()
        if not user:
            return make_response({"message": "Invalid credentials"}, 401)
        if check_password_hash(user.password, password):
            now = datetime.now(timezone.utc)
            expire = now + timedelta(minutes=60)

            token = jwt.encode(
                {
                    "email": user.email, 
                    "id": user.id,
                    "expiry" : expire.isoformat()
                }, 
                "secret",
                "HS256")
            return make_response({"token": token}, 200)
        
        else:
            return make_response({"message": "Invalid credentials"}, 401)
    else:
        return make_response({"message": "Invalid data"}, 401)  
    

@app.route("/", methods=["GET"])
def root():
    return make_response({"message": "Fund manager APIs"}, 200)



def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None 
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            if not token:
                return make_response({"message": "User not authorized"}, 401)
            try:
                data = jwt.decode(token, "secret", algorithms=["HS256"])
                current_user = User.query.filter_by(id=data['id']).first()
            except Exception as e:
                return make_response({"message": "User not authorized"}, 401)
            return f(current_user, *args, **kwargs)
        else:
            return make_response({"message": "User not authorized"}, 401)
        
    return decorated



@app.route("/funds", methods=["GET"])
@token_required
def get_all_funds(current_user):
    funds = Fund.query.filter_by(user_id=current_user.id).all()
    if funds:
        totalSum = Fund.query.with_entities(db.func.round(db.func.sum(Fund.amount)),2).filter_by(user_id=current_user.id).all()[0][0]
    return make_response( jsonify({
        "data":[ row.serialize for row in funds ],
        "sum": totalSum
    }), 200)


@app.route("/funds", methods=['POST'])
@token_required
def postFund(current):
    data = request.json
    if data["amount"]:
        fund = Fund(
            amount=data["amount"],
            user_id=current.id
        )
        db.session.add(fund)
        db.session.commit()
        print(fund)
    else:
        return make_response({"message": "Invalid data"}, 401)
    return make_response({"message": "Fund added successfully"}, 200)


@app.route("/funds/<id>", methods=['PUT'])
@token_required
def updateFund(current, id):
    try:
        funds = Fund.query.filter_by(user_id=current.id, id=id).first()
        if funds == None:
            return {"message":"Unable to update"}, 409
        data = request.json
        if data["amount"]:
            funds.amount = data["amount"]
        db.session.commit()
        return {"message":funds.serialize}, 200
    except Exception as e:
        print(e)
        return {"error":"Unable to process"}, 409
    

@app.route("/funds/<id>", methods=['DELETE'])
@token_required
def deleteFund(current, id):
    try:
        funds = Fund.query.filter_by(user_id=current.id, id=id).first()
        if funds == None:
            return {"message":f"Fund with {id} not found"}, 404
        db.session.delete(funds)
        db.session.commit()
        return {"message":"Deleted"}, 202
    except Exception as e:
        print(e)
        return {"error":"Unable to process"}, 409

