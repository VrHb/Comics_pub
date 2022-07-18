# Публикация комиксов

Проект публикует комиксы с сайта [xkcd](https://xkcd.com) в группу VK.

## Как установить

* Необходимо установить интерпретатор python версии 3.10
* Cкопировать содержимое проекта к себе в рабочую директорию
* Активировать внутри рабочей директории виртуальное окружение:
```
python -m venv [название окружения]
```
* Установить зависимости(необходимые библиотеки):
```
pip install -r requirements.txt
```

### Настройка переменных окружения:

* Для хранения переменных окружения создаем файл .env:
```
touch .env
```
* [Регистрируем приложение VK](https://vk.com/dev) и получаем ключ приложения для использования API VK
по этой [ссыслке](https://vk.com/dev/implicit_flow_user), записываем в .env файл:
```
echo "VK_TOKEN='ваш ключ'" >> .env
```
* Добавляем id группы в VK, куда будем публиковать посты:
```
echo "VK_GROUP_ID='id группы'" >> .env
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
