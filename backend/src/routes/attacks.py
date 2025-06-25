from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.engine import db
from models.role import Role
from models.user import User
import os
import psutil
from core.remote_attacker import *
#пересмотреть список подключаемых библиотек

attacks_bp = Blueprint('attacks', __name__)

@attacks_bp.route('/attacks/nmap-scan', methods=['POST'])
@jwt_required()  # Требуется JWT-токен для доступа
def nmap_scan():
    """
    Роут для запуска nmap-сканирования на удаленной машине Kali Linux.
    """
    # Получаем данные из JSON-запроса
    data = request.get_json()
    target_subnet = data.get("target_subnet")
    kali_ip = data.get("kali_ip")
    
    # Проверяем, что переданы все необходимые параметры
    if not target_subnet or not kali_ip:
        return jsonify({"error": "Необходимо указать 'target_subnet' и 'kali_ip'"}), 400
    
    # Параметры для Kali Linux
    kali_port = 22              # Порт SSH
    kali_user = "kali"          # Имя пользователя
    kali_password = "kali"      # Пароль

    # Подключаемся к Kali Linux
    ssh_client = connect_to_kali(kali_ip, kali_port, kali_user, kali_password)
    if not ssh_client:
        return jsonify({"error": "Не удалось подключиться к Kali Linux"}), 500

    try:
        # Запускаем nmap-сканирование
        result, status_code = run_nmap_scan(ssh_client, target_subnet)
        return jsonify(result), status_code
    finally:
        # Закрываем соединение
        if ssh_client:
            ssh_client.close()
            print("Соединение с Kali Linux закрыто.")

@attacks_bp.route('/attacks/opensmtpd-exploit', methods=['POST'])
@jwt_required()  # Раскомментируйте, если требуется JWT-аутентификация
def opensmtpd_exploit():
    """
    Роут для эксплуатации уязвимости OpenSMTPD (CVE-2020-7247).
    """
    # Получаем данные из JSON-запроса
    data = request.get_json()
    target_ip = data.get("target_subnet")
    kali_ip = data.get("kali_ip")
    
    # Проверяем, что переданы все необходимые параметры
    if not target_ip or not kali_ip:
        return jsonify({"error": "Необходимо указать 'target_ip' и 'kali_ip'"}), 400
    
    # Параметры для Kali Linux
    kali_port = 22              # Порт SSH
    kali_user = "kali"          # Имя пользователя
    kali_password = "kali"      # Пароль

    # Подключаемся к Kali Linux
    ssh_client = connect_to_kali(kali_ip, kali_port, kali_user, kali_password)
    if not ssh_client:
        return jsonify({"error": "Не удалось подключиться к Kali Linux"}), 500

    try:
        # Запускаем эксплуатацию OpenSMTPD
        result, status_code = exploit_opensmtpd(ssh_client, target_ip)
        return jsonify(result), status_code
    finally:
        # Закрываем соединение
        if ssh_client:
            ssh_client.close()
            print("Соединение с Kali Linux закрыто.")

@attacks_bp.route('/attacks/vsftpd-msf-exploit', methods=['POST'])
def vsftpd_msf_exploit():
    """
    Роут для эксплуатации уязвимости vsftpd 2.3.4 через Metasploit.
    """
    data = request.get_json()
    target_ip = data.get("target_subnet")
    kali_ip = data.get("kali_ip")
    
    if not target_ip or not kali_ip:
        return jsonify({"error": "Необходимо указать 'target_ip' и 'kali_ip'"}), 400
    
    kali_port = 22
    kali_user = "kali"
    kali_password = "kali"

    ssh_client = connect_to_kali(kali_ip, kali_port, kali_user, kali_password)
    if not ssh_client:
        return jsonify({"error": "Не удалось подключиться к Kali Linux"}), 500

    try:
        result, status_code = exploit_vsftpd_with_msf(ssh_client, target_ip)
        return jsonify(result), status_code
    finally:
        if ssh_client:
            ssh_client.close()
            print("Соединение с Kali Linux закрыто.")

@attacks_bp.route('/attacks/mikrotik-msf-exploit', methods=['POST'])
def mikrotik_msf_exploit():
    """
    Роут для эксплуатации уязвимости vsftpd 2.3.4 через Metasploit.
    """
    data = request.get_json()
    target_ip = data.get("target_subnet")
    kali_ip = data.get("kali_ip")
    
    if not target_ip or not kali_ip:
        return jsonify({"error": "Необходимо указать 'target_ip' и 'kali_ip'"}), 400
    
    kali_port = 22
    kali_user = "kali"
    kali_password = "kali"

    ssh_client = connect_to_kali(kali_ip, kali_port, kali_user, kali_password)
    if not ssh_client:
        return jsonify({"error": "Не удалось подключиться к Kali Linux"}), 500

    try:
        result, status_code = exploit_mikrotik(ssh_client, target_ip)
        return jsonify(result), status_code
    finally:
        if ssh_client:
            ssh_client.close()
            print("Соединение с Kali Linux закрыто.")

@attacks_bp.route('/attacks/juice-shop-login-sqli', methods=['POST'])
def juice_shop_login_sqli():
    """
    Роут для эксплуатации SQL Injection в методе /rest/user/login через SSH на Kali Linux.
    """
    data = request.get_json()
    juice_shop_ip = data.get("target_subnet")
    kali_ip = data.get("kali_ip")
    email_payload = data.get("email_payload", "' OR 1=1 --")  # По умолчанию стандартная SQLi

    if not juice_shop_ip or not kali_ip:
        return jsonify({"error": "Необходимо указать 'juice_shop_ip' и 'kali_ip'"}), 400

    kali_port = 22
    kali_user = "kali"
    kali_password = "kali"

    ssh_client = connect_to_kali(kali_ip, kali_port, kali_user, kali_password)
    if not ssh_client:
        return jsonify({"error": "Не удалось подключиться к Kali Linux"}), 500

    try:
        result, status_code = exploit_juice_shop_login(ssh_client, juice_shop_ip, email_payload)
        return jsonify(result), status_code
    finally:
        if ssh_client:
            ssh_client.close()
            print("Соединение с Kali Linux закрыто.")

@attacks_bp.route('/attacks/dirb', methods=['POST'])
def juice_shop_dirb():
    """
    Роут для запуска dirb на Juice Shop через Kali Linux.
    """
    data = request.get_json()
    juice_shop_ip = data.get("target_subnet")
    kali_ip = data.get("kali_ip")

    if not juice_shop_ip or not kali_ip:
        return jsonify({"error": "Необходимо указать 'target_subnet' и 'kali_ip'"}), 400

    kali_port = 22
    kali_user = "kali"
    kali_password = "kali"

    # Подключаемся к Kali Linux
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh_client.connect(kali_ip, port=kali_port, username=kali_user, password=kali_password)
        print("Подключение успешно установлено.")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return jsonify({"error": "Не удалось подключиться к Kali Linux"}), 500

    try:
        # Формируем URL для Juice Shop
        juice_shop_url = f"http://{juice_shop_ip}"
        result, status_code = run_dirb_on_kali(ssh_client, juice_shop_url)
        return jsonify(result), status_code
    finally:
        if ssh_client:
            ssh_client.close()
            print("Соединение с Kali Linux закрыто.")
            