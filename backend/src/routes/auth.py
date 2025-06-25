from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import db, User
from decorators import route_required

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify(msg='User already exists'), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(msg='User created successfully'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(
            access_token=access_token,
            username=username  
        ), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    # Проверяем, что все необходимые данные предоставлены
    if not username or not old_password or not new_password:
        return jsonify({"msg": "Missing required fields"}), 400

    # Находим пользователя в базе данных
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Проверяем старый пароль
    if not user.check_password(old_password):
        return jsonify({"msg": "Old password is incorrect"}), 400

    # Обновляем пароль пользователя
    user.set_password(new_password)
    db.session.commit()

    return jsonify({
            "msg": "Password changed successfully"
        }), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
@route_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(msg=f'Logged in as user ID: {current_user_id}')