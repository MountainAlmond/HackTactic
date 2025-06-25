import os
import sys
import subprocess
import time
import re
from threading import Thread

class VirtualBoxManager:
    def __init__(self):
        self.inventory_dir = "../../auto-deploy/ansible/inventory/"  # Папка для хранения inventory-файлов
        self.playbook_dir = "../../auto-deploy/ansible"   # Папка с playbook-ами
        os.makedirs(self.inventory_dir, exist_ok=True)  # Создаем папку, если её нет

    def run_command(self, command):
        """Выполнение команды через subprocess."""
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Ошибка выполнения команды: {e.stderr}")
            sys.exit(1)

    def create_vm(self, ova_path, host_adapter, ram_gb, cpu_count, disk_gb):
        """
        Создание новой виртуальной машины.
        :param ova_path: Путь к OVA-файлу.
        :param host_adapter: Имя сетевого адаптера хоста.
        :param ram_gb: Объем RAM в ГБ.
        :param cpu_count: Количество CPU.
        :param disk_gb: Размер диска в ГБ.
        """
        # Проверка корректности числовых параметров
        if not (ram_gb.isdigit() and int(ram_gb) > 0):
            print("Ошибка: RAM должен быть положительным целым числом (в ГБ).")
            sys.exit(1)

        if not (cpu_count.isdigit() and int(cpu_count) > 0):
            print("Ошибка: Количество CPU должно быть положительным целым числом.")
            sys.exit(1)

        if not (disk_gb.isdigit() and int(disk_gb) > 0):
            print("Ошибка: Размер диска должен быть положительным целым числом (в ГБ).")
            sys.exit(1)

        # Генерация уникального имени для виртуальной машины
        base_name = "VM"
        vm_name = base_name
        counter = 1
        existing_vms = self.run_command(["VBoxManage", "list", "vms"])
        while vm_name in existing_vms:
            vm_name = f"{base_name}-{counter}"
            counter += 1

        print(f"Сгенерировано уникальное имя виртуальной машины: {vm_name}")

        # Проверка существования OVA-файла
        if not os.path.isfile(ova_path):
            print(f"Ошибка: OVA-файл не найден по пути {ova_path}")
            sys.exit(1)

        # Проверка существования сетевого адаптера хоста
        try:
            subprocess.run(["ip", "link", "show", host_adapter], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print(f"Ошибка: Сетевой интерфейс '{host_adapter}' не найден на хосте.")
            sys.exit(1)

        # Генерация пути к целевому диску
        target_disk_path = f"../../images/{vm_name}-disk001.vdi"

        # Удаление старого диска (если существует)
        if os.path.exists(target_disk_path):
            print(f"Удаление старого диска: {target_disk_path}")
            os.remove(target_disk_path)

        # Импорт OVA-файла с изменением размера диска
        print("Импорт OVA-файла с изменением размера диска...")
        self.run_command([
            "VBoxManage", "import", ova_path,
            "--vsys", "0",
            "--vmname", vm_name,
            "--cpus", cpu_count,
            "--memory", str(int(ram_gb) * 1024),
            "--unit", "14", "--disk", target_disk_path
        ])

        # Изменение размера диска
        if int(disk_gb) > 20:
            print(f"Изменение размера диска до {disk_gb}ГБ...")
            self.run_command(["VBoxManage", "modifymedium", "disk", target_disk_path, "--resize", str(int(disk_gb) * 1024)])

        # Настройка сетевого моста
        print(f"Настройка сетевого моста на интерфейсе {host_adapter}...")
        self.run_command(["VBoxManage", "modifyvm", vm_name, "--nic1", "bridged", "--bridgeadapter1", host_adapter])

        # Запуск виртуальной машины
        print("Запуск виртуальной машины...")
        self.run_command(["VBoxManage", "startvm", vm_name, "--type", "gui"])

        # #Бывают проблемы с BusyBox Kali (поэтому делаем рестарт VM)
        # if "Kali" in ova_path:
        #     print("Ожидание 30сек...")
        #     time.sleep(30)
        #     print("Перезапуск виртуальной машины...")
        #     self.run_command(["VBoxManage", "controlvm", vm_name, "poweroff"])
        #     self.run_command(["VBoxManage", "startvm", vm_name, "--type", "gui"])
        #     time.sleep(20)

        print("Теперь выполните следующие действия:")
        print(f"1. Войдите в VM {vm_name}")
        return vm_name
    
    def find_vm_ip(self, vm_name, subnet="192.168.0", retries=3, delay=3):
        """
        Поиск IP-адреса виртуальной машины по её MAC-адресу с повторными попытками.
        :param vm_name: Имя виртуальной машины.
        :param subnet: Подсеть для поиска (например, 192.168.0).
        :param retries: Количество повторных попыток.
        :param delay: Задержка между попытками (в секундах).
        :return: IP-адрес виртуальной машины или None, если не удалось найти.
        """
        # Получение MAC-адреса виртуальной машины
        print(f"Получение MAC-адреса виртуальной машины '{vm_name}'...")
        vminfo = self.run_command(["VBoxManage", "showvminfo", vm_name])
        if not vminfo:
            print(f"Ошибка: Не удалось получить информацию о ВМ '{vm_name}'.")
            return None

        mac_match = re.search(r"MAC:\s+([0-9A-F]{12})", vminfo, re.IGNORECASE)
        if not mac_match:
            print(f"Ошибка: Не удалось найти MAC-адрес для ВМ '{vm_name}'.")
            return None

        mac_address = mac_match.group(1)
        mac_address_formatted = ":".join(mac_address[i:i + 2] for i in range(0, 12, 2))
        print(f"MAC-адрес виртуальной машины: {mac_address_formatted}")

        # Повторные попытки поиска IP-адреса
        attempt = 1
        while attempt <= retries:
            print(f"Попытка {attempt} из {retries}: Поиск IP-адреса...")

            # Пингование всех IP-адресов в подсети
            print("Пингование всех IP-адресов в подсети...")
            processes = []
            for ip in range(1, 255):
                target_ip = f"{subnet}.{ip}"
                process = subprocess.Popen(
                    ["ping", "-c", "1", "-W", "1", target_ip],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                processes.append(process)

            # Ожидание завершения всех ping-процессов
            for process in processes:
                process.wait()

            # Поиск IP-адреса по MAC-адресу в таблице ARP
            print("Поиск IP-адреса для MAC-адреса...Ожидание заполнения ARP-таблицы")
            time.sleep(delay)  # Задержка для обновления ARP-таблицы
            arp_table = self.run_command(["arp", "-a"])
            if not arp_table:
                print("Ошибка: Не удалось получить ARP-таблицу.")
                return None

            ip_match = re.search(rf"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+{mac_address_formatted}", arp_table, re.IGNORECASE)
            if ip_match:
                ip_address = ip_match.group(1)
                print(f"IP-адрес найден: {ip_address}")
                return ip_address

            print(f"IP-адрес не найден. Повторная попытка через {delay} секунд...")
            time.sleep(delay)
            attempt += 1

        print(f"Ошибка: Не удалось найти IP-адрес для MAC-адреса {mac_address_formatted} после {retries} попыток.")
        return None

    def delete_vm(self, vm_name):
        """
        Принудительное удаление виртуальной машины.
        :param vm_name: Имя виртуальной машины.
        """
        print(f"Принудительное удаление виртуальной машины '{vm_name}'...")

        try:
            # 1. Проверяем, существует ли виртуальная машина
            existing_vms = self.run_command(["VBoxManage", "list", "vms"])
            if vm_name not in existing_vms:
                print(f"Ошибка: Виртуальная машина '{vm_name}' не найдена.")
                return

            # 2. Если машина запущена, принудительно останавливаем её
            running_vms = self.run_command(["VBoxManage", "list", "runningvms"])
            if vm_name in running_vms:
                print(f"Виртуальная машина '{vm_name}' запущена. Принудительная остановка...")
                self.run_command(["VBoxManage", "controlvm", vm_name, "poweroff"])

            # 3. Удаляем виртуальную машину
            print(f"Удаление виртуальной машины '{vm_name}'...")
            print(f"Ожидание 10 сек перед удалением")
            time.sleep(10)
            self.run_command(["VBoxManage", "unregistervm", vm_name, "--delete"])

            print(f"Виртуальная машина '{vm_name}' успешно удалена.")

        except Exception as e:
            print(f"Ошибка при удалении виртуальной машины: {e}")
            
            self.delete_inventory(vm_name)

            print(f"Виртуальная машина '{vm_name}' успешно удалена.")
    
    def poweroff_vm(self, vm_name):
        """
        Выключение виртуальной машины.
        :param vm_name: Имя виртуальной машины.
        """
        print(f"Выключение виртуальной машины '{vm_name}'...")

        try:
            # 1. Проверяем, существует ли виртуальная машина
            existing_vms = self.run_command(["VBoxManage", "list", "vms"])
            if vm_name not in existing_vms:
                print(f"Ошибка: Виртуальная машина '{vm_name}' не найдена.")
                return

            # 2. Проверяем, запущена ли виртуальная машина
            running_vms = self.run_command(["VBoxManage", "list", "runningvms"])
            if vm_name not in running_vms:
                print(f"Виртуальная машина '{vm_name}' уже выключена.")
                return

            # 3. Выполняем принудительное выключение
            print(f"Выключение виртуальной машины '{vm_name}'...")
            self.run_command(["VBoxManage", "controlvm", vm_name, "poweroff"])

            print(f"Виртуальная машина '{vm_name}' успешно выключена.")

        except Exception as e:
            print(f"Ошибка при выключении виртуальной машины: {e}")
    
    def start_vm(self, vm_name, headless=True):
        """
        Запуск виртуальной машины.
        :param vm_name: Имя виртуальной машины.
        :param headless: Запускать машину в фоновом режиме (без графического интерфейса).
        """
        print(f"Запуск виртуальной машины '{vm_name}'...")

        try:
            # 1. Проверяем, существует ли виртуальная машина
            existing_vms = self.run_command(["VBoxManage", "list", "vms"])
            if vm_name not in existing_vms:
                print(f"Ошибка: Виртуальная машина '{vm_name}' не найдена.")
                return

            # 2. Проверяем, запущена ли виртуальная машина
            running_vms = self.run_command(["VBoxManage", "list", "runningvms"])
            if vm_name in running_vms:
                print(f"Виртуальная машина '{vm_name}' уже запущена.")
                return

            # 3. Запускаем машину
            print(f"Запуск виртуальной машины '{vm_name}'...")
            if headless:
                self.run_command(["VBoxManage", "startvm", vm_name, "--type", "gui"])
            else:
                self.run_command(["VBoxManage", "startvm", vm_name])

            print(f"Виртуальная машина '{vm_name}' успешно запущена.")

        except Exception as e:
            print(f"Ошибка при запуске виртуальной машины: {e}")
    
    def restart_vm(self, vm_name):
        """
        Перезагрузка виртуальной машины.
        :param vm_name: Имя виртуальной машины.
        """
        print(f"Перезагрузка виртуальной машины '{vm_name}'...")

        try:
            # 1. Проверяем, существует ли виртуальная машина
            existing_vms = self.run_command(["VBoxManage", "list", "vms"])
            if vm_name not in existing_vms:
                print(f"Ошибка: Виртуальная машина '{vm_name}' не найдена.")
                return

            # 2. Проверяем, запущена ли виртуальная машина
            running_vms = self.run_command(["VBoxManage", "list", "runningvms"])
            if vm_name not in running_vms:
                print(f"Ошибка: Виртуальная машина '{vm_name}' не запущена. Запуск машины...")
                self.run_command(["VBoxManage", "startvm", vm_name, "--type", "gui"])
                print(f"Виртуальная машина '{vm_name}' запущена.")
            else:
                print(f"Виртуальная машина '{vm_name}' запущена. Выполняется перезагрузка...")
                self.run_command(["VBoxManage", "controlvm", vm_name, "reset"])

            print(f"Виртуальная машина '{vm_name}' успешно перезагружена.")

        except Exception as e:
            print(f"Ошибка при перезагрузке виртуальной машины: {e}")
    
    def create_inventory(self, vm_ip, vm_name, username="osimages", password="Osimages123!"):
        """
        Создание inventory-файла для Ansible.
        :param vm_ip: IP-адрес виртуальной машины.
        :param vm_name: Имя виртуальной машины.
        :param username: Имя пользователя для подключения к VM.
        :param password: Пароль для подключения к VM.
        """
        inventory_content = f"""[all]
{vm_name} ansible_host={vm_ip} ansible_ssh_user={username} ansible_ssh_pass={password} ansible_sudo_pass={password}
"""
        inventory_file = os.path.join(self.inventory_dir, f"{vm_name}.ini")
        with open(inventory_file, "w") as f:
            f.write(inventory_content)

        print(f"Inventory файл создан: {inventory_file}")
        return inventory_file
    
    def delete_inventory(self, vm_name):
        """
        Удаление inventory-файла для виртуальной машины.
        :param vm_name: Имя виртуальной машины.
        :return: True, если файл успешно удален, иначе False.
        """
        inventory_file = os.path.join(self.inventory_dir, f"{vm_name}.ini")
        
        if os.path.exists(inventory_file):
            try:
                os.remove(inventory_file)
                print(f"Inventory файл удален: {inventory_file}")
                return True
            except Exception as e:
                print(f"Ошибка при удалении inventory-файла: {e}")
                return False
        else:
            print(f"Inventory файл не найден: {inventory_file}")
            return False
    
    def run_ansible_playbook(self, inventory_file, playbook_name):
        """
        Запуск Ansible playbook с выводом логов в реальном времени и возвратом результата.
        :param inventory_file: Путь к inventory-файлу.
        :param playbook_name: Название playbook-а.
        :return: True, если playbook завершился успешно, иначе False.
        """
        playbook_path = os.path.join(self.playbook_dir, playbook_name)
        print(f"Playbook: {playbook_path}")
        print(f"Inventory: {inventory_file}")
        if not os.path.exists(playbook_path):
            print(f"Ошибка: Playbook не найден по пути {playbook_path}")
            return False

        command = [
            "ansible-playbook",
            "-i", inventory_file,
            playbook_path,
            "--ssh-common-args='-o StrictHostKeyChecking=no'"
        ]

        # Создаем объект для хранения результата выполнения
        result_container = {"success": False}

        def run_and_store_result():
            """Запускает playbook и сохраняет результат."""
            result_container["success"] = self._run_playbook_in_background(command)

        # Запуск playbook в фоне
        thread = Thread(target=run_and_store_result)
        thread.start()
        thread.join()  # Дожидаемся завершения выполнения

        # Возвращаем результат выполнения
        return result_container["success"]
    
    def _run_playbook_in_background(self, command):
        """
        Выполнение Ansible playbook в фоне с выводом логов в реальном времени.
        :param command: Команда для запуска playbook-а.
        :return: True, если playbook завершился успешно, иначе False.
        """
        try:
            print("Запуск Ansible playbook...")
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # Чтение и вывод логов в реальном времени
            for line in process.stdout:
                print(line, end="")

            # Ожидание завершения процесса
            process.wait()

            if process.returncode != 0:
                print(f"Ansible playbook завершился с ошибкой (код {process.returncode})")
                return False
            else:
                print("Ansible playbook успешно завершен.")
                return True

        except Exception as e:
            print(f"Ошибка при выполнении Ansible playbook: {e}")
            return False

    def configure_vm_with_ansible(self, vm_name, playbook_name, subnet="192.168.0", username="osimages", password="Osimages123!"):
        """
        Настройка виртуальной машины с помощью Ansible.
        :param vm_name: Имя виртуальной машины.
        :param playbook_name: Название playbook-а.
        :param subnet: Подсеть для поиска IP-адреса.
        :param username: Имя пользователя для подключения к VM.
        :param password: Пароль для подключения к VM.
        """
        # Поиск IP-адреса VM
        vm_ip = self.find_vm_ip(vm_name, subnet)
        if not vm_ip:
            print(f"Ошибка: Не удалось найти IP-адрес для VM '{vm_name}'.")
            return

        print(f"IP-адрес VM '{vm_name}': {vm_ip}")

        # Создание inventory-файла
        inventory_file = self.create_inventory(vm_ip, vm_name, username, password)

        # Запуск Ansible playbook
        self.run_ansible_playbook(inventory_file, playbook_name)

    def create_and_configure_vm(self, ova_path, host_adapter, ram_gb, cpu_count, disk_gb, playbooks, subnet="192.168.0"):
        """
        Создание VM и запуск нескольких Ansible playbook-ов последовательно.
        :param ova_path: Путь к OVA-файлу.
        :param host_adapter: Сетевой адаптер хоста.
        :param ram_gb: Количество RAM (в ГБ).
        :param cpu_count: Количество CPU.
        :param disk_gb: Размер диска (в ГБ).
        :param playbooks: Список названий playbook-ов для запуска.
        :param subnet: Подсеть для поиска IP-адреса.
        :return: Словарь с информацией о VM или сообщение об ошибке.
        """
        # Шаг 1: Создание VM
        vm_name = self.create_vm(ova_path, host_adapter, ram_gb, cpu_count, disk_gb)
        if not vm_name:
            return {"success": False, "error": "Не удалось создать виртуальную машину."}

        print("Ожидание запуска виртуальной машины...")
        time.sleep(80)  # Даем время для загрузки VM
        if "Microtik" in ova_path:
            return {"success": True, "success": "Инициализирована ВМ микротик, донастройте в консоли"}
        if "ActiveDirectory" in ova_path:
            time.sleep(300)
            vm_ip = self.find_vm_ip(vm_name, subnet)
            return {"success": True, "vm_name": vm_name, "ip_address": vm_ip}

        # Шаг 4: Поиск IP-адреса VM
        vm_ip = self.find_vm_ip(vm_name, subnet)
        if not vm_ip:
            return {"success": False, "error": f"Не удалось найти IP-адрес для VM '{vm_name}'."}

        # Шаг 5: Создание inventory-файла
        inventory_file = self.create_inventory(vm_ip, vm_name)

        # Шаг 6: Запуск playbook-ов последовательно
        all_playbooks_successful = True
        for playbook in playbooks:
            success = self.run_ansible_playbook(inventory_file, playbook)
            if not success:
                all_playbooks_successful = False
                break  # Прекращаем выполнение, если один из playbook-ов завершился с ошибкой

        if all_playbooks_successful:
            return {"success": True, "vm_name": vm_name, "ip_address": vm_ip}
        else:
            return {"success": False, "error": "Произошла ошибка при настройке виртуальной машины."}

