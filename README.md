# HTTP Client
Автор: Сычев Иван Валерьевич ФТ-104-2

## Описание
Консольный HTTP Client, который может отправлять GET, HEAD, POST, PUT запросы и принимать ответы сервера.
Результат это файл с заголовками ответа, сам полученный файл и изображения полученные из него
по прямым ссылкам. 

Дополнительная информация в help по команде: `http_client -h`

## Требования
* Использование библиотеки socket

## Состав
* Запуск из `http_client.py`
* Работа с сетью: `network.py`
* Тесты: `tests.py`
* Запись файлов: `utils.py`

## Примеры верных команд

http_client https://www.python.org GET

http_client https://www.python.org GET -v 1.1 -he "Connection: Keep-Alive, Accept-Language: fr"

http_client https://www.python.org POST

http_client https://www.python.org POST -v 1.1 -he "Connection: Keep-Alive, Accept-Language: fr" -d "Test message"

http_client https://www.python.org PUT

http_client https://www.python.org PUT -v 1.1 -he "Connection: Keep-Alive, Accept-Language: fr" -d "Test message"

http_client https://www.python.org HEAD

http_client https://www.python.org HEAD -v 1.1 -he "Connection: Keep-Alive, Accept-Language: fr"
