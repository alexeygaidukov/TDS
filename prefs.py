APACHE_USER = "www-data"                        # используется в init.py для создания Sqlite базы.
APACHE_GROUP = "www-data"                       # используется в init.py для создания Sqlite базы.
DATA_PATH = "/var/www/upload/tds"               # папка, где хранится Sqlite база и ШМД
SITE_URL = "/arximed/hs/confprovider"           # Часть URL публикации сервиса

CHECK_ITS_USER = False                           # Выполнять проверку логину на ИТС. Для локальных публикаций рекомендуется отключать
VALID_ITS_USERS = ['test']                      # Только указанные ИТС Логины смогут публиковать на сервере публикаций ШМД
FNSI_userkey = "uuid"


# В словаре (dict) ключ - имя конфигурации, значение - актуальная версия. Версия указывается с точностью до 3-го числа, то есть номер сборки игонорируется.

CONFIGS = {
    'МедицинаБольница':
        "2.0.6", 
    'МедицинаПоликлиника':
        "3.0.6"
}
