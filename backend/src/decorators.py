from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import request, jsonify
from models.user import User

def route_required():
    """
    Декоратор для проверки доступа к маршруту на основе роли пользователя.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Проверка наличия JWT-токена
            verify_jwt_in_request()

            # Получение ID пользователя из токена
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user:
                return jsonify(msg="User not found"), 404

            # Получение текущего маршрута
            current_route = request.path

            # Проверка доступа к маршруту
            if not user.has_route_access(current_route):
                return jsonify(msg="Access denied"), 403

            return fn(*args, **kwargs)

        return decorator
    return wrapper