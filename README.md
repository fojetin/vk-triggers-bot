# ВК триггер бот
Бот по зволяет задавать триггеры группе через админку на Django
Предназначен для одной группы.

# Установка
```
git clone https://github.com/fojetin/vk-triggers-bot.git
cd vk-triggers-bot

python3 -venv venv
. venv/bin/activate
pip install -r requirements.txt

./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
###### Авто деплой на heroku.com
![](https://img.shields.io/appveyor/ci/fojetin/vk-triggers-bot.svg)
