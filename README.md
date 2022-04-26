#http_client

Автор задачи: Сычев Иван Валерьевич ФТ-104-2

Запуск из http_client.py

Примеры верных команд:

http_client https://www.python.org GET

http_client https://www.python.org GET -v 1.1 -he "Connection: Keep-Alive, Accept-Language: fr"

http_client https://www.python.org POST

http_client https://www.python.org POST -v 1.1 -he "Connection: Keep-Alive, Accept-Language: fr" -d "Test message"

http_client https://www.python.org PUT

http_client https://www.python.org PUT -v 1.1 -he "Connection: Keep-Alive, Accept-Language: fr" -d "Test message"

http_client https://www.python.org HEAD

http_client https://www.python.org HEAD -v 1.1 -he "Connection: Keep-Alive, Accept-Language: fr"

Дополнительная информация в help по команде:

http_client -h
