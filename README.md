# tds - сервис распространения ШМД для 1С:Медицина

Сервис распространения [шаблонов медицинских документов (ШМД)](https://solutions.1c.ru/catalog/clinic/emr) для 1С:Медицина служит для централизованного хранения ШМД. 
Сервис может использоваться в региональных проектах, когда ведется внедрение 1С:Медицина в нескольких медицинских организациях. Обслуживающая организация может публиковать ШМД в 
сервисе, а ИТ службы медицинских организаций могут получать ШМД из централизованного сервиса, установленного в защищенной сети региональной системы здравоохранения.

ШМД хранятся в сервисе в привязка к версии и наименовании конфигурации. Версия конфигурации берется без учета номера сборки (последнее число версии). 

## Описание структуры проекта
### init.py - создание SQLite базы

База создается в папке, заданной в переменной ``DATA_PATH`` файла ``prefs.py``. Для получения доступа из веб сервера к базе необходимо задать переменные ``APACHE_USER`` и ``APACHE_GROUP`` в файле ``prefs.py`` значениями, которые использует веб сервер. Папке, указанной в ``DATA_PATH`` необходимо установить владельца и группу теми же значениями, 
которые использует веб сервер.

В этой же папке, указанной в переменной ``DATA_PATH``, будут размещаться сохраненные ШМД. Рекомендуется эту папку размещать на томе с файловой системой ``ntfs``, поскольку на практике могут встречаться ШМД, имена которых состоят из 128 кириллических букв и более, которые в кодировке ``UTF-8`` требуют 256 байт и более, а имена файлов в файловой системе ``ext4``, стандартной для операционной системы linux, не могут превышать 255 байт.

### prefs.py - настройки сервиса 
В переменной  CONFIGS задаются имена конфигурации и их актуальные версиии. Версия указывается с точностью до 3-го числа, то есть номер сборки игнорируется.

Переменные:
- ``CHECK_ITS_USER`` - выполнять проверку логину на ИТС. Для локальных публикаций рекомендуется отключать.
- ``VALID_ITS_USERS`` - только указанные в списке ИТС Логины смогут публиковать на сервере публикаций ШМД.
- ``FNSI_userkey`` - токен пользователя сайта nsi.rosminzdrav.ru. Использутеся для получения справочников "Типы МД" и "Типы РЭМД" с ФНСИ. Допускается пустое значение. См. https://its.1c.ru/db/instrpoly3#content:1040:1:issogl1_16.7.1_взаимодействие_с_фнси

После внесения изменений в файл может потребоваться перезапуск веб сервера, чтобы настройки применились.


### tds.wsgi - основной скрипт
В скрипте реализованы следующие методы сервиса
#### /CVS/Hello/{ТикетИТС}
Авторизация в сервисе. В случае когда ``CHECK_ITS_USER=True``, то выполняется проверка тикета на login.1c.ru. Это позволяет ограничить доступ к сервису для пользователей, 
которые не имеют действующией подписки на ИТС. 

Если ``CHECK_ITS_USER=False``, то тогда параметр ТикетИТС интерпретируется как имя пользователя сервиса (см. список ``VALID_ITS_USERS``). 

Метод возвращает УидСессии. 
 
#### /CVS/MDT/{УидСессии}/{ИмяМетода}
Выполнение действий с базой ШМД. Операции: 
- ``GetFile`` - получение ШМД
- ``UploadFile`` - добавляет ШМД в базу сервиса. Пользователь, определенный для сессии в ``/CVS/Hello``, должен присутствовать в списке ``VALID_ITS_USERS``.
- ``DeleteFile`` - удаляет ШМД из базы сервиса. Пользователь, определенный для сессии в ``/CVS/Hello``, должен присутствовать в списке ``VALID_ITS_USERS``.
- ``GetList`` - возращает список ШМД, загруженных в сервис
Параметр УидСессии должен содержать сведения об актуальной сессии.

#### /getTeplatesList
Возвращает html со списком ШМД, загруженных в сервис распространения ШМД, для акутальной версии 1С:Медицина. Больница. Для корректной работы метода необходимо задать корректное значение переменной ``FNSI_userkey``.

#### /getFullTeplatesList
Возвращает html с полным списком ШМД, загруженных в сервис распространения ШМД.

## Установка
1) Подключить модуль ``mod_wsgi`` из пакета ``libapache2-mod-wsgi-py3``
2) Скопировать файлы ``tds.wsgi``, ``prefs.py``, ``init.py`` в папку ``/var/www/wsgi/tds``
3) Внести настройки экземпляра сервиса в ``prefs.py``
4) Запустить ``init.py``
5) Зарегистрировать приложение WSGI в конфигурации apache2
```
	WSGIScriptAlias /wsgi/tds /var/www/wsgi/tds/tds.wsgi
```
6) В файле ``/etc/apache2/envvars`` установить локаль в UTF-8
```
	LANG="ru_RU.UTF-8"
```
