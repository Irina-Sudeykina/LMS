# Проект "LMS-система" - Платформа для онлайн-обучения

## Описание:
 Проект "LMS" - это проект на Python, 
 передставляющи собой платформу для онлайн-обучения
 
## Установка:
 1. Клонируйте репозиторий:
 ```
 git clone https://github.com/Irina-Sudeykina/LMS.git
 
 ```

 2. Установите зависимости:
 ```
 pip install -r requirements.txt
 ```

## Использование:

### Модель User: ###
Модель представляет пользователя платформы, и имеет следующие свойства:<br>
email - Email,<br>
phone - Телефон,<br>
sity - Город<br>
avatar - Аватар<br>

### Модель Payment: ###
Модель представляет платежи пользователя платформы, и имеет следующие свойства:<br>
user - Пользователь,<br>
date_payment - Дата оплаты,<br>
сourse - Курс<br>
lesson - Урок,<br>
amount - Сумма оплаты,<br>
method - Способ оплаты<br>
session_id - id сессии<br>
link - Ссылка на оплату<br>

### Модель Subscription: ###
Модель представляет подписки пользователя платформы, и имеет следующие свойства:<br>
user - Пользователь,<br>
сourse - Курс<br>
is_subscription - статус подписки<br>


### Контроллер UserViewSet(ModelViewSet) ###
Контроллер для CRUD операций по пользователям платформы

### Контроллер PaymentFilter(FilterSet) ###
Контроллер точной фильтрации по способу оплаты.
Определяем жестко допустимые методы оплаты.

### Контроллер PaymentViewSet(ModelViewSet) ###
Контроллер для CRUD операций по платежам

### Контроллер SubscriptionViewSet(ModelViewSet) ###
Контроллер для операций по подпискам



### Модель Сourse: ###
Модель представляет обучающий курс, и имеет следующие свойства:<br>
title - Название курса,<br>
preview - Превью,<br>
description - Описание курса<br>
owner - Владелец курса<br>
updated_at - Дата и время последнего изменения<br>

### Модель Lesson: ###
Модель представляет урок, и имеет следующие свойства:<br>
title - Название урока,<br>
description - Описание урока<br>
preview - Превью,<br>
video_url - Ссылка на видео,<br>
сourse - Курс,<br>
owner - Владелец урока<br>


### Контроллер СourseViewSet(ModelViewSet) ###
Контроллер для CRUD операций по курсам

### Контроллер LessonCreateAPIView(CreateAPIView) ###
Контроллер для сздания урока

### Контроллер LessonListAPIView(ListAPIView) ###
Контроллер для просмотра списка уроков

### Контроллер LessonRetrieveAPIView(RetrieveAPIView) ###
Контроллер для просмотра конкретного урока

### Контроллер LessonUpdateAPIView(UpdateAPIView) ###
Контроллер для редактирования урока

### Контроллер LessonDestroyAPIView(DestroyAPIView) ###
Контроллер для удаления урока


## Функции:

### Функция create_stripe_product(title) ###
Создает продукт в stripe<br>
Принимает: <br>
 title - название продукта<br>

### Функция create_stripe_price(product, amount) ###
Создает цену в stripe<br>
Принимает: <br>
 product - продукт<br>
 amount - цена продукта<br>

### Функция create_stripe_sessions(price) ###
Создает продукт в stripe<br>
Принимает: <br>
 price - цена продукта<br>



## Задачи:

### Задача send_information_update_course(email_list, title) ###
Отложенная задача отправки уведомлений об обновлении курса

### Задача deactivate_inactive_users() ###
Периодическая задача блокировки неактивных пользователей


## Запуск сервера:
В терминале выполните:
 ```
python manage.py runserver
 ```
Для остановки нажмите Ctrl + C



 ## Тестирование:
Проект покрыт тестами фреймворка DRF. Для их запуска выполните команду:
```
python manage.py test
или
coverage run --source='.' manage.py test
```
Для выгрузки отчета о покрытии проекта тестами выполните команду:
```
coverage report
или
coverage html
```

## Документация:
http://localhost:8000/swagger/
или
http://localhost:8000/redoc/

## Лицензия:
Проект распространяется под [лицензией MIT](LICENSE).
