# khblog

Итак у нас имеетсся проект на гитхабе. Django, nginx, docker, postgresql.

Развертываем на сервере(облаке).

Создаем сервер, покупаем


ssh-keygen для ssh ключа с подключением через него

~/.ssh/id_rsa.pub здесь ключ и копируем его в настройках для подключения к серверу на сервисе, где берете VPS

Подключаемся к серверу ssh root@ip.ip.ip.ip

клонируем репозиторий git clone

устанавливаем docker https://www.digitalocean.com/community/tutorials/docker-ubuntu-18-04-1-ru

устанавливаем docker-compose https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-16-04

устанавливаем nginx $ apt-get install nginx

запускаем билдинг docker-compose up --build path to docker-compose.yaml


