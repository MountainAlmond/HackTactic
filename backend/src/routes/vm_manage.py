from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.vm_manager import VirtualBoxManager  # Импортируем класс VirtualBoxManager

# Создаем Blueprint для управления виртуальными машинами
vm_bp = Blueprint('vm', __name__)

# Экземпляр VirtualBoxManager для выполнения операций
vm_manager = VirtualBoxManager()

@vm_bp.route('/vm/create', methods=['POST'])
@jwt_required()
def create_vm():
    """
    Создание новой виртуальной машины.
    Требует JSON с параметрами: ova_path, host_adapter, ram_gb, cpu_count, disk_gb.
    """
    current_user_id = get_jwt_identity()  # Получаем ID текущего пользователя
    data = request.get_json()

    required_fields = ['ova_path', 'host_adapter', 'ram_gb', 'cpu_count', 'disk_gb']
    if not all(field in data for field in required_fields):
        return jsonify(error="Missing required fields"), 400

    try:
        vm_name = vm_manager.create_vm(
            ova_path=data['ova_path'],
            host_adapter=data['host_adapter'],
            ram_gb=data['ram_gb'],
            cpu_count=data['cpu_count'],
            disk_gb=data['disk_gb']
        )
        return jsonify(msg=f"VM '{vm_name}' created successfully"), 201
    except Exception as e:
        return jsonify(error=str(e)), 500


@vm_bp.route('/vm/delete/<string:vm_name>', methods=['POST'])
# @jwt_required()
def delete_vm(vm_name):
    """
    Удаление виртуальной машины.
    :param vm_name: Имя виртуальной машины.
    """
    # current_user_id = get_jwt_identity()
    try:
        vm_manager.delete_vm(vm_name)
        return jsonify(msg=f"VM '{vm_name}' deleted successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@vm_bp.route('/vm/start/<string:vm_name>', methods=['POST'])
# @jwt_required()
def start_vm(vm_name):
    """
    Запуск виртуальной машины.
    :param vm_name: Имя виртуальной машины.
    """
    # current_user_id = get_jwt_identity()
    try:
        vm_manager.start_vm(vm_name)
        return jsonify(msg=f"VM '{vm_name}' started successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@vm_bp.route('/vm/stop/<string:vm_name>', methods=['POST'])
# @jwt_required()
def stop_vm(vm_name):
    """
    Остановка виртуальной машины.
    :param vm_name: Имя виртуальной машины.
    """
    # current_user_id = get_jwt_identity()
    try:
        vm_manager.poweroff_vm(vm_name)
        return jsonify(msg=f"VM '{vm_name}' stopped successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@vm_bp.route('/vm/restart/<string:vm_name>', methods=['POST'])
# @jwt_required()
def restart_vm(vm_name):
    """
    Перезагрузка виртуальной машины.
    :param vm_name: Имя виртуальной машины.
    """
    # current_user_id = get_jwt_identity()
    try:
        vm_manager.restart_vm(vm_name)
        return jsonify(msg=f"VM '{vm_name}' restarted successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@vm_bp.route('/vm/find_ip/<string:vm_name>', methods=['GET'])
@jwt_required()
def find_vm_ip(vm_name):
    """
    Поиск IP-адреса виртуальной машины.
    :param vm_name: Имя виртуальной машины.
    """
    current_user_id = get_jwt_identity()
    try:
        ip_address = vm_manager.find_vm_ip(vm_name)
        if ip_address:
            return jsonify(ip=ip_address), 200
        else:
            return jsonify(error="Failed to find IP address"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500


@vm_bp.route('/vm/configure/<string:vm_name>', methods=['POST'])
@jwt_required()
def configure_vm(vm_name):
    """
    Настройка виртуальной машины с помощью Ansible playbook.
    Требует JSON с параметром: playbook_name.
    :param vm_name: Имя виртуальной машины.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if 'playbook_name' not in data:
        return jsonify(error="Missing playbook_name"), 400

    try:
        vm_manager.configure_vm_with_ansible(
            vm_name=vm_name,
            playbook_name=data['playbook_name']
        )
        return jsonify(msg=f"VM '{vm_name}' configured successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@vm_bp.route('/vm/create-ubuntu', methods=['POST'])
def create_ubuntu_api():
    try:
        # Получаем данные из запроса
        data = request.json
        cpu_count = data.get('cpuCount')
        ram_gb = data.get('ramGb',)
        disk_gb = data.get('diskGb')
        
        vm_info = vm_manager.create_and_configure_vm(
            ova_path="../../images/Ubuntu_Server.ova",  # Убедитесь, что путь корректен
            host_adapter="wlx242fd02d27eb",               # Убедитесь, что адаптер существует
            ram_gb=str(ram_gb),                                   # Передаем число вместо строки
            cpu_count=str(cpu_count),                                 # Передаем число вместо строки
            disk_gb=str(disk_gb),                                 # Передаем число вместо строки
            playbooks=[],  # Список playbook-ов
            subnet="192.168.0"                           # Подсеть для поиска IP
        )
        
        # Возвращаем результат
        return jsonify({
            "success": True,
            "vm_name": vm_info['vm_name'],
            "ip_address": vm_info['ip_address'],
            "status": "created"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500

@vm_bp.route('/vm/create-elk', methods=['POST'])
def create_elk_api():
    try:
        # Получаем данные из запроса
        data = request.json
        cpu_count = data.get('cpuCount')
        ram_gb = data.get('ramGb',)
        disk_gb = data.get('diskGb')
        
        vm_info = vm_manager.create_and_configure_vm(
            ova_path="../../images/Ubuntu_Server.ova",  # Убедитесь, что путь корректен
            host_adapter="wlx242fd02d27eb",               # Убедитесь, что адаптер существует
            ram_gb=str(ram_gb),                                   # Передаем число вместо строки
            cpu_count=str(cpu_count),                                 # Передаем число вместо строки
            disk_gb=str(disk_gb),                                 # Передаем число вместо строки
            playbooks=['extend_disk.yml', 'elk_install.yml'],  # Список playbook-ов
            subnet="192.168.0"                           # Подсеть для поиска IP
        )
        
        # Возвращаем результат
        return jsonify({
            "success": True,
            "vm_name": vm_info['vm_name'],
            "ip_address": vm_info['ip_address'],
            "status": "created"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500

@vm_bp.route('/vm/create-kali', methods=['POST'])
def create_kali_api():
    try:
        # Получаем данные из запроса
        data = request.json
        cpu_count = data.get('cpuCount')
        ram_gb = data.get('ramGb',)
        disk_gb = data.get('diskGb')
        
        vm_info = vm_manager.create_and_configure_vm(
            ova_path="../../images/Kali.ova",  # Убедитесь, что путь корректен
            host_adapter="wlx242fd02d27eb",               # Убедитесь, что адаптер существует
            ram_gb=str(ram_gb),                                   # Передаем число вместо строки
            cpu_count=str(cpu_count),                                 # Передаем число вместо строки
            disk_gb=str(disk_gb),                                 # Передаем число вместо строки
            playbooks=[],  # Список playbook-ов
            subnet="192.168.0"                           # Подсеть для поиска IP
        )
        
        # Возвращаем результат
        return jsonify({
            "success": True,
            "vm_name": vm_info['vm_name'],
            "ip_address": vm_info['ip_address'],
            "status": "created"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500

@vm_bp.route('/vm/create-vuln', methods=['POST'])
def create_vuln_api():
    try:
        # Получаем данные из запроса
        data = request.json
        cpu_count = data.get('cpuCount')
        ram_gb = data.get('ramGb',)
        disk_gb = data.get('diskGb')
        
        vm_info = vm_manager.create_and_configure_vm(
            ova_path="../../images/Ubuntu_Server.ova",  # Убедитесь, что путь корректен
            host_adapter="wlx242fd02d27eb",               # Убедитесь, что адаптер существует
            ram_gb=str(ram_gb),                                   # Передаем число вместо строки
            cpu_count=str(cpu_count),                                 # Передаем число вместо строки
            disk_gb=str(disk_gb),                                 # Передаем число вместо строки
            playbooks=['docker.yml', 'compose.yml', 'vulnlab.yml'],  # Список playbook-ов
            subnet="192.168.0"                           # Подсеть для поиска IP
        )
        
        # Возвращаем результат
        return jsonify({
            "success": True,
            "vm_name": vm_info['vm_name'],
            "ip_address": vm_info['ip_address'],
            "status": "created"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500

@vm_bp.route('/vm/create-mikrotik', methods=['POST'])
def create_vuln_mikrotik():
    try:
        # Получаем данные из запроса
        data = request.json
        cpu_count = data.get('cpuCount')
        ram_gb = data.get('ramGb',)
        disk_gb = data.get('diskGb')
        
        vm_info = vm_manager.create_and_configure_vm(
            ova_path="../../images/Mikrotik.ova",  # Убедитесь, что путь корректен
            host_adapter="wlx242fd02d27eb",               # Убедитесь, что адаптер существует
            ram_gb=str(ram_gb),                                   # Передаем число вместо строки
            cpu_count=str(cpu_count),                                 # Передаем число вместо строки
            disk_gb=str(disk_gb),                                 # Передаем число вместо строки
            playbooks=[],                                   # Список playbook-ов
            subnet="192.168.0"                           # Подсеть для поиска IP
        )
        
        # Возвращаем результат
        return jsonify({
            "success": True,
            "vm_name": vm_info['vm_name'],
            "ip_address": vm_info['ip_address'],
            "status": "created"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500

@vm_bp.route('/vm/create-ad', methods=['POST'])
def create_vuln_ad():
    try:
        # Получаем данные из запроса
        data = request.json
        cpu_count = data.get('cpuCount')
        ram_gb = data.get('ramGb',)
        disk_gb = data.get('diskGb')
        
        vm_info = vm_manager.create_and_configure_vm(
            ova_path="../../images/ActiveDirectory.ova",  # Убедитесь, что путь корректен
            host_adapter="wlx242fd02d27eb",               # Убедитесь, что адаптер существует
            ram_gb=str(ram_gb),                                   # Передаем число вместо строки
            cpu_count=str(cpu_count),                                 # Передаем число вместо строки
            disk_gb=str(disk_gb),                                 # Передаем число вместо строки
            playbooks=[],                                   # Список playbook-ов
            subnet="192.168.0"                           # Подсеть для поиска IP
        )
        
        # Возвращаем результат
        return jsonify({
            "success": True,
            "vm_name": vm_info['vm_name'],
            "ip_address": vm_info['ip_address'],
            "status": "created"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500
