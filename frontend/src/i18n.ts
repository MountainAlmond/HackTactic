import i18n from "i18next";
import { initReactI18next } from "react-i18next";


const resources = {
  en: {
    translation: {
      navbar: {
        "InfraModels": "Infrastructure models",
        "Attacks": "Attack Scenarios",
        "Results": "Attack results",
        "SIEM": "In SIEM",
        "Create_user": "Create User",
        "about": "About system",
        "rules": "Rules",
      },
      "usage_rules": {
        "title": "System Usage Rules",
        "general_title": "General Rules",
        "general_text": "Before conducting cybersecurity training, the administrator must prepare information about the deployed infrastructure and give to members",
        "blue_team_title": "Rules for the Blue Team",
        "blue_team_text": "The administrator must provide participants with access to ELK (login, password, address) for event analysis and anomaly detection.",
        "red_team_title": "Rules for the Red Team",
        "red_team_text": "For the red team participants, a prepared Kali VM image is provided (for interaction via the web) or access to a specially prepared Kali image for manual attack execution."
      },
      availableRegsList: {
        "title": "Voting list with open registration"
      },
      auth_form: {
        "Product_name": "Hack tactic",
        "Login": "Login",
        "Registration": "Registration",
        "Username": "username",
        "Password": "password",
        "Enter": "Login",
        "Dont_have": "Don't have an account?",
        "Here": "Register here",
        "Already": "Already have an account?",
        "If_forget": "*Don't have an account or forget password? Please contact your system administrator.",
        "Change_password_link": "Change base password",
        "Change_password": "Change password",
        "Old_password": "Old password",
        "New_password": "New password",
        "Confirm_password": "Confirm password",
        "Change": "Change",
        "Back_to_login": "Back to login",

        //информация об ошибках и прочие информационные сообщения
        "Username_is_req": "Username is required",
        "Password_is_req": "Password is required",
        "Old_password_is_req": "Enter old password",
        "New_password_is_req": "Enter new password",
        "Confirm_password_is_req": "Enter confirm password",
        "Password_min_length": "Min length is 8 symbols",
        "Passwords_must_match": "Passwords must match",
      },
      system_description: {
        title: "Automated Network Attack Modeling System",
        purpose: "Purpose of the system",
        purpose_text: "The system is designed for automatic deployment of information infrastructure stands and configuration of cybersecurity tools, saving time on preparation and focusing on cybersecurity training.",
        features: "Main features",
        blue_team_training: "Blue team training",
        blue_team_desc: "Working with ELK SIEM & IDS Suricata for event analysis and anomaly detection after conducting network attacks.",
        red_team_training: "Red team training",
        red_team_desc: "Ability to practice various attacks (manually and using a library of scripts) to improve penetration testing skills and understanding of how cybersecurity tools work based on ELK SIEM and IDS Suricata.",
        contributors_title: "Contributors",
        developed_by_department: "Developed by the Department of Computer Security and Mathematical Support of Information Systems:",
        developer: "Denis Olegovich Povyshyov (Student) - Developer",
        supervisor: "Irina Valeryevna Vlatskaya (PhD, Associate Professor, Head of the Department of Computer Security and Mathematical Support of Information Systems) - Project Supervisor"
      },
      create_user_form: {
        "Create_User": "Create User",
        "User_created_success": "User successfully created",
        "Unknown_error": "An unknown error occurred",
        "Username": "Username",
        "Password": "Password",
        "Confirm_password": "Confirm Password",
        "Submit": "Create",
    
        // Information about errors and other messages
        "Username_is_req": "Username is required",
        "Password_is_req": "Password is required",
        "Confirm_password_is_req": "Please confirm the password",
        "Password_min_length": "Minimum password length is 8 characters",
        "Passwords_must_match": "Passwords must match"
    },
      popup_redirect: {
        "Confirm": "Confirm",
        "Message": "Do you want go to SIEM?",
        "Y": "Yes",
        "N": "No"
      },

      //кнопки на карточке инфраструктуры и общие элементы
      "infra_grid": {
        "Show_Details": "Details",
        "Start": "Deploy",
        "Restart": "Start",
        "Stop": "Stop",
        "Delete": "Delete",
        "Close": "Close",
        "Create": "Create",
        "Cancel": "Cancel"
      },

      //описания инфраструктур (пока лучше ничего не придумал)
      "infrastructure.items.service_1": "Ubuntu Server",
"infrastructure.descriptions.service_1": "A clean Ubuntu server, nothing extra",
"infrastructure.full_descriptions.service_1": "Ubuntu 20.04, a stable version with a basic set of programs and utilities onboard",

"infrastructure.items.service_2": "Kali",
"infrastructure.descriptions.service_2": "The Swiss Army knife for pentesters",
"infrastructure.full_descriptions.service_2": "At least one Kali Linux instance is required to practice attack scripts. Feel like a real pentester!",

"infrastructure.items.service_3": "Vulnerable Lab on Docker",
"infrastructure.descriptions.service_3": "Containers with vulnerabilities for every taste",
"infrastructure.full_descriptions.service_3": "You can find more details on GitHub: https://github.com/DarkRelay-Security-Labs/vulnlab_aws",

"infrastructure.items.service_4": "MikroTik Router",
"infrastructure.descriptions.service_4": "Vulnerable virtual MikroTik.",
"infrastructure.full_descriptions.service_4": "Vulnerable network equipment, hmm, an easy target for breaching through the DMZ.",

"infrastructure.items.service_5": "Microsoft AD",
"infrastructure.descriptions.service_5": "Vulnerable Active Directory domain",
"infrastructure.full_descriptions.service_5": "Launch Kali! I hope the terms DCSync, Kerberos, SMB, NTLM are familiar to you...",

"infrastructure.items.service_7": "ELK Stack",
"infrastructure.descriptions.service_7": "Open Source SIEM (contact your administrator for credentials) To go to SIEM, specify <VM IP:5601>",
"infrastructure.full_descriptions.service_7": "At least one instance is needed so the Blue Team can analyze alerts. If you have issues with the Elastic password, contact the system administrator.",
      
      
      //Переводы для элементов атак
      "attack_scripts": {
        "Run": "Run",
        "Running": "Running...",
        "View_Results": "View Results",
        "Close": "Close",
        "Execution_Result": "Execution Result",
        "Target_Subnet": "Target Subnet or address",
        "Kali_IP": "Kali IP",
        "Enter_Target_Subnet": "Enter target subnet or IP (e.g., 192.168.0.0/24)",
        "Enter_Kali_IP": "Enter Kali Linux IP address",
        "Error_No_Data": "Please fill in all fields.",
        "Error_Script_Failed": "An error occurred while running the script."
      },
      "attack_script_1_name": "OpenSMTPD Attack (Mail Server Mayhem)",
      "attack_script_1_description": "Exploiting OpenSMTPD to run arbitrary code — because who doesn't love a good mail server meltdown?",
      "attack_script_1_full_description": "Using an OpenSMTPD vulnerability to take over the mail server. Perfect for sending 'emails' on behalf of the admin — phishing has never been this fun!",
      "attack_script_2_name": "Nmap Port Scanner (Reconnaissance Rodeo)",
      "attack_script_2_description": "Scanning the network for open ports and active services — because you can't hack what you can't see!",
      "attack_script_2_full_description": "Running Nmap to find out which doors are open in the system. It's like ringing every apartment doorbell until someone answers!",
      "attack_script_3_name": "VSFTPD Metasploit Attack (FTP Fiasco)",
      "attack_script_3_description": "Exploiting VSFTPD to gain system access — because FTP servers deserve some love too!",
      "attack_script_3_full_description": "Exploiting a VSFTPD vulnerability to gain root access. It's like finding a secret entrance to a club, except instead of a password, it's a bug!",
      "attack_script_4_name": "SQL Injection (Database Dive)",
      "attack_script_4_description": "Using SQL injection to extract user data — because databases should always share their secrets!",
      "attack_script_4_full_description": "Breaking  SQL injection. If databases could talk, they'd probably ask us to stop!",
      "attack_script_5_name": "Directory Busting",
      "attack_script_5_description": "Automated directory and file enumeration to discover hidden resources.",
      "attack_script_5_full_description": "We use Dirb to scan the target website for hidden directories and files. If there's something valuable hidden in the depths of the web server, Dirb will find it. It's like a treasure hunt, but with HTTP requests.",  
      "attack_script_6_name": "Mikrotik(CVE-2018-14847)",
      "attack_script_6_description": "Old MikroTik firmware with WinBox read vulnerability.",
      "attack_script_6_full_description": "Let's make the router share its secrets. Metasploit should know something about CVE-2018-14847."
      
    


    }
  },
  ru: {
    translation: {
      navbar: {
        "InfraModels": "Инфраструктурные модели",
        "Attacks": "Сценарии атак",
        "Results": "Результаты атак",
        "SIEM": "В SIEM",
        "Create_user": "Создать пользователя",
        "about": "О системе",
        "rules": "Правила",
      },
      "usage_rules": {
        "title": "Правила использования системы",
        "general_title": "Общие правила",
        "general_text": "Перед проведением обучения по кибербезопасности администратор должен составить информацию о развернутой инфраструктуре и предоставить ее участникам.",
        "blue_team_title": "Правила для синей команды",
        "blue_team_text": "Администратор должен предоставить участникам возможность подключения к ELK (логин, пароль, адрес) для анализа событий и выявления аномалий.",
        "red_team_title": "Правила для красной команды",
        "red_team_text": "Для участников красной команды предоставляется образ подготовленной ВМ Kali (для взаимодействия через веб) или доступ к специально подготовленному образу Kali для проведения атак вручную."
      },
      availableRegsList: {
        "title": "Список голосований с открытой регистрацией"
      },
      auth_form: {
        "Product_name": "Hack tactic",
        "Login": "Вход",
        "Registration": "Регистрация",
        "Username": "имя пользователя",
        "Password": "пароль",
        "Enter": "Войти",
        "Dont_have": "Еще нет аккаунта?",
        "Here": "Зарегестрироваться",
        "Already": "Уже есть аккаунт?",
        "If_forget": "*Еще нет аккаунта или забыли пароль? Пожалуйста, обратитесь к вашему системному администратору",
        "Change_password_link": "Сменить стандартный пароль",
        "Change_password": "Сменить пароль",
        "Old_password": "Старый пароль",
        "New_password": "Новый пароль",
        "Confirm_password": "Подтверждение пароля",
        "Change": "Сменить",
        "Back_to_login": "Вернуться к форме входа",

        //информация об ошибках и прочие информационные сообщения
        "Username_is_req": "Имя обязательно",
        "Password_is_req": "Пароль обязателен",
        "Old_password_is_req": "Введите старый пароль",
        "New_password_is_req": "Введите новый пароль",
        "Confirm_password_is_req": "Введите подтверждение пароля",
        "Password_min_length": "Минимальная длина 8 символов",
        "Passwords_must_match": "Пароли должны совпадать",
      },
      create_user_form: {
        "Create_User": "Создать пользователя",
        "User_created_success": "Пользователь успешно создан",
        "Unknown_error": "Произошла неизвестная ошибка",
        "Username": "Имя пользователя",
        "Password": "Пароль",
        "Confirm_password": "Подтверждение пароля",
        "Submit": "Создать",
    
        // Информация об ошибках и прочие информационные сообщения
        "Username_is_req": "Имя пользователя обязательно",
        "Password_is_req": "Пароль обязателен",
        "Confirm_password_is_req": "Подтвердите пароль",
        "Password_min_length": "Минимальная длина пароля 8 символов",
        "Passwords_must_match": "Пароли должны совпадать"
      },
      system_description: {
        title: "Автоматизированная система моделирования сетевых атак",
        purpose: "Назначение системы",
        purpose_text: "Система предназначена для автоматической развертки стендов информационных инфраструктур и настройки средств обеспечения кибербезопасности, что позволяет экономить время на подготовку и сосредоточиться на обучении кибербезопасности.",
        features: "Основные возможности",
        blue_team_training: "Тренировка синей команды",
        blue_team_desc: "Работа с ELK SIEM & IDS Suricata для анализа событий и выявления аномалий после проведения сетевых атак.",
        red_team_training: "Тренировка красной команды",
        red_team_desc: "Возможность отработки различных атак (вручную и с помощью библиотеки скриптов) для повышения навыков тестирования на проникновение и понимания работы инструментов обеспечения кибербезопасности на основе ELK SIEM и IDS Suricata.",
        contributors_title: "Авторы",
        developed_by_department: "Разработано кафедрой компьютерной безопасности и математического обеспечения информационных систем:",
        developer: "Повышев Денис Олегович (студент) - разработчик",
        supervisor: "Влацкая Ирина Валерьевна (кандидат технических наук, доцент, заведующая кафедрой КБ МОИС) - руководитель проекта"
      },
      
      popup_redirect: {
        "Confirm": "Подтерждение",
        "Message": "Вы хотите перейти в SIEM?",
        "Y": "Да",
        "N": "Нет"
      },


      //кнопки на карточке инфраструктуры и общие элементы
      "infra_grid": {
        "Show_Details": "Подробнее",
        "Start": "Деплой",
        "Restart": "Старт",
        "Stop": "Стоп",
        "Delete": "Удалить",
        "Close": "Закрыть",
        "Create": "Создать",
        "Cancel": "Отмена"
      },
      //описания инфраструктур (пока лучше ничего не придумал, как просто писать в файлик с переводами)
      "infrastructure.items.service_1": "Ubuntu Сервер",
      "infrastructure.descriptions.service_1": "Чистый сервер на Ubuntu, ничего лишнего",
      "infrastructure.full_descriptions.service_1": "Ubuntu 20_04, стабильная версия, базовый набор программ и утилит на борту",
      
    
      "infrastructure.items.service_2": "Kali",
      "infrastructure.descriptions.service_2": "Швейцарский нож пентестера",
      "infrastructure.full_descriptions.service_2": "Для отработки скриптов атак необходим хотя бы один инстанс Kali Linux. Почувствуй себя пентестером!",
      
    
      "infrastructure.items.service_3": "Уязвимая лаборатория на Docker",
      "infrastructure.descriptions.service_3": "Контейнеры с уязвимостями на любой вкус",
      "infrastructure.full_descriptions.service_3": "Подробное описание можешь найти на github: https://github.com/DarkRelay-Security-Labs/vulnlab_aws",
      
      "infrastructure.items.service_4": "Маршрутизатор MikroTik",
      "infrastructure.descriptions.service_4": "Уязвимый виртуальный Mikrotik.",
      "infrastructure.full_descriptions.service_4": "Уязвимое сетевое оборудование, ммм, легкая мешень для прохода через DMZ",

      "infrastructure.items.service_5": "Microsoft AD",
      "infrastructure.descriptions.service_5": "Уязвимый домен Active Directory",
      "infrastructure.full_descriptions.service_5": "Запускай Kali! Надеюсь, слова DCSync, Kerberos, SMB, NTLM тебе знакомы...",

      "infrastructure.items.service_7": "Стек ELK",
      "infrastructure.descriptions.service_7": "Open Source SIEM (для получения учетных данных обратитесь к вашему администратору) Для перехода в SIEM укажите <IP VM:5601>",
      "infrastructure.full_descriptions.service_7": "Нужен хотя бы один инстанс, чтобы Blue Team мог анализировать сработки, при проблемах с паролем от elastic обратитесь к системному администратору",
      

      "attack_scripts": {
        "Run": "Запустить",
        "Running": "Выполняется...",
        "View_Results": "Посмотреть результаты",
        "Close": "Закрыть",
        "Execution_Result": "Результат выполнения",
        "Target_Subnet": "Целевая подсеть или адрес",
        "Kali_IP": "IP Kali Linux",
        "Enter_Target_Subnet": "Введите целевую подсеть или адрес (например, 192.168.0.0/24)",
        "Enter_Kali_IP": "Введите IP-адрес Kali Linux",
        "Error_No_Data": "Пожалуйста, заполните все поля.",
        "Error_Script_Failed": "Произошла ошибка при выполнении скрипта."
      },
      "attack_script_1_name": "Атака на OpenSMTPD (почтовый сервер)",
        "attack_script_1_description": "Эксплуатация уязвимости в OpenSMTPD для выполнения произвольного кода.",
        "attack_script_1_full_description": "Используем уязвимость в OpenSMTPD, чтобы захватить контроль над почтовым сервером. Идеально подходит для тех, кто хочет отправить 'письма' от имени администратора!",
        "attack_script_2_name": "Сканер портов Nmap",
        "attack_script_2_description": "Сканирование сети на открытые порты и активные сервисы.",
        "attack_script_2_full_description": "Запускаем Nmap, чтобы узнать, какие двери открыты в системе. Это как звонить во все квартиры, пока кто-нибудь не откроет.",
        "attack_script_3_name": "Атака на VSFTPD через Metasploit",
        "attack_script_3_description": "Использование уязвимости в VSFTPD для получения доступа к системе.",
        "attack_script_3_full_description": "Эксплуатируем уязвимость в VSFTPD, чтобы получить root-доступ. Это как найти секретный вход в клуб, только вместо пароля — баг.",
        "attack_script_4_name": "SQL-инъекция",
        "attack_script_4_description": "Атака с использованием SQL-инъекции для получения данных пользователей.",
        "attack_script_4_full_description": "Ломаем авторизацию через SQL-инъекцию. Если бы базы данных могли говорить, они бы точно попросили нас остановиться.",
        "attack_script_5_name": "Перебор директорий",
        "attack_script_5_description": "Автоматизированный перебор директорий и файлов для обнаружения скрытых ресурсов.",
        "attack_script_5_full_description": "Мы используем Dirb для сканирования целевого сайта в поисках скрытых директорий и файлов. Если на сервере спрятано что-то ценное, Dirb это найдет. Это как охота за сокровищами, только с HTTP-запросами.",

        "attack_script_6_name": "Mikrotik(CVE-2018-14847)",
        "attack_script_6_description": "Старая прошивка Mikrotik с уязвимостью чтения в WinBox",
        "attack_script_6_full_description": "Заставим роутер поделиться своими секретами. Metasploit должен что-то знать про CVE-2018-14847",
    }
  }
};

i18n
  .use(initReactI18next) // passes i18n down to react-i18next
  .init({
    resources,
    lng: "ru", // language to use, more information here: https://www.i18next.com/overview/configuration-options#languages-namespaces-resources
    // you can use the i18n.changeLanguage function to change the language manually: https://www.i18next.com/overview/api#changelanguage
    // if you're using a language detector, do not define the lng option

    interpolation: {
      escapeValue: false // react already safes from xss
    }
  });

  export default i18n;