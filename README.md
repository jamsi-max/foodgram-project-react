# ✨Foodgram✨

### **Продуктовый помощник с возможностью скачивния списка покупок в PDF**
##### Стек технологий: 
##### Frontend - **React (HTML, CSS, JS)**
##### Backend - **Django (DRF), PostgreSQL, NGINX**
#
##### `Проект реализован по принципу CI/CD`
#

##### **Домашняя страница:** `http://eda.sytes.net/`

![](https://github.com/jamsi-max/foodgram-project-react/blob/master/backend/data_for_db/foodgram.png?raw=true)

###### В проекте реализовано

- все сервисы и страницы доступны для пользователей в соответствии с их правами;
- рецепты на всех страницах сортируются по дате публикации (новые — выше);
- рецепты фильтруются по тегам;
- добавление рецептов в избранное;
- подписка на авторов;
- добавление рецептов в покупики;
- скачивание списка продуктов в формате PDF(ингридиенты ссумируются из всех добавленных в покупки рецептов);
- регистрация пользователей и смена пароля;

## **Запуск проекта локально**
##### 1. Клонировать репозиторий
#
```sh
git clone https://github.com/jamsi-max/foodgram-project-react.git
```
##### 2. Сооздать файл ".env" в папке infra с содержанием по примеру .env.sample
#
##### 3. Из директории "footgram\infra", где находиться файл **"docker-compose.yaml"**  выполнить команду в консоле для запуска проекта в контейнерах:
`Внимание! Docker уже должен быть установлен и запущен`
```sh
docker-compose up -d
```
##### 4. Создать суперпользователя:
#
```sh
docker-compose run --rm backend sh -c "python manage.py createsuperuser"
```
##### 5. Внимание! Статика и миграции выполняются в автоматическом режиме
#
### Документация проекта по адресу http://localhost/redoc
#
##### Для остановки проекта используйте команду:
#
```sh
docker-compose down
```
## Лицензия

MIT

**Бесплатный софт**
##### Автор проекта: Макс
##### Связь с автором(телеграмм): https://t.me/jony2024 
##### © Copyright **[jamsi-max](https://github.com/jamsi-max)**

