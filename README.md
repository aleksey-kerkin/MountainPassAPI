# Проект виртуальной стажировки онлайн-школы Skillfactory
## Документация
### Проект опубликован на хостинге amvera.ru

https://mountainpass-aleksey-kerkin.amvera.io/

### Документация сгенерирована с помощью пакета drf-spectacular

Документация swagger: https://mountainpass-aleksey-kerkin.amvera.io/api/schema/swagger-ui/

Документация redoc: https://mountainpass-aleksey-kerkin.amvera.io/api/schema/redoc/

## Описание проекта
### Мобильное приложение для оправки информации туристами о посещённых ими горных перевалов.

Мобильное приложение для Android и IOS, пользователями которого будут туристы. В горах они будут вносить данные о перевале в приложение и отправлять их в ФСТР ( Федерация спортивного туризма России ), как только появится доступ в Интернет, для того чтобы поделиться информацией с другими людьми, увлеющимися туризмом и преодолением горных перевалов.
## Работа проекта
### Внесение личной информации.

Для отправки информации туристу необходимо будет заполнить данные о себе (регистрация не требуется):
1. Фамилия
2. Имя
3. Отчество
4. Электронная почта
5. Номер телефона

### Внесение информации о горном перевале.

Для отправки информации о горном перевале, туристу необходимо будет также заполнить несколько полей:
1. Название горного перевала
2. Альтернативное название горного перевала
3. Произвольный текст ввиде комментария
4. Координаты горного перевала
5. Сложность восхождения (в зависимости от времени года)

### Обработка информации.

Модератор из федерации будет верифицировать и вносить в базу данных информацию, полученную от пользователей, а те в свою очередь смогут увидеть в мобильном приложении статус модерации и просматривать базу с объектами, внесёнными другими.

## Содержание проекта

### Основные пункты.

* Проект выполнен на языке программирования Python
* С использованием фреймворка Django
* В проекте используется СУБД PostgreSQL

### Модели проекта.

Модель пользователя `Tourist` содержит 5 полей для заполнения данных о пользователе:
* 3 поля `CharField` для заполения данных
* 1 поле `PhoneNumber` для указания телефонного номера
* 1 поле `EmailField` для указания электронной почты

Модель `Coord` служит для указания координат горного перевала и имеет 3 поля:
* 2 поля `DecimalField` для указания широты и долготы
* 1 поле `IntegerField` для указания высоты

Модель `Level` служит для указания уровня сложности восхождения на тот или иногй горный перевал:
* Имеет 4 поля `CharField` в каждом из которых необходимо выбрать уровень сложности восхождения от 1А до 4A

Основной моделью проекта является модель `MountainPass` включающая в себя 9 полей:
* 4 поля `CharField` включающие в себя общее название, название и альтернативное название горного перевала, а таже поле `status` с выбором статуса модерации.
* 1 поле `DateTimeField` для даты добавления горного перевала
* Поля `level` и `tourist_id` имеющие отношения один ко многим с соответствующими моделями
* Поле `coord_id` имеющее отношение один к одному с соответствующей моделью

Модель `Image` служит для добавления фото горного перевала, имеет 3 поля:
* Поле `pereval_id` имеющее имеющие отношения один ко многим с соответствующей моделью
* Поле `image` имеющее тип `ImageField` для добавления изображений либо ссылки на него
* А также поле `title` для обозначения названия изображения



### Сериализаторы проекта.

Каждая модель проекта имеет соответствующий сериализатор.
Основным сериализатором проекта служит `MountainPassSerializer` содержащий в себе сериализаторы остальных моделей.

```
class MountainPassSerializer(WritableNestedModelSerializer):
    tourist_id = TourisSerializer()
    coord_id = CoordSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)
    
```

### Представления и маршрутизация проекта.

В качестве представлений в проекте используется наследование класса `ModelViewSet`.
В проекте используются url, предоставляющий список всех добавленных перевалов от пользователей
`path('', include(router.urls)),` 
Можно просмотреть информацию об отдельном перевале по id.
При этом есть возможность использовать CRUD методы, а также фильтровать добавленную информацию по электронной почте пользователя.

### Ограничения в проекте.

В проекте существует условие при котором пользователь может изменить отправленные данные:
1. Данные не должны относиться к данным о самом пользователе (фамилия, имя, телефон и т.д.)
2. Статус модерации данной информации должен быть статусом 'NW', при остальных статусах модерации, изменение данных невозможно.

### Метод:

POST/submitData/
принимает JSON в теле запроса с информацией о перевале. Пример JSON-a:



       {     
        "beauty_title": "title_1",
        "title": "title_1",
        "other_titles": "title_1",
        "connect": "title_1",
        "tourist_id": {
           
            "email": "ivanov@gmail.ru",
            "last_name": "Иванов",
            "first_name": "Иван",
            "middle_name": "Иванович",
            "phone": "+7(999)9999999"
        },
        "coord_id": {
            
            "latitude": 54.87690019,
            "longitude": 43.36759009,
            "height": 1244
        },
        "level": {
           
            "winter_lev": "4A",
            "spring_lev": "2A",
            "summer_lev": "1A",
            "autumn_lev": "3A"
        },
        "images": []
    }

Результат метода: JSON

status — код HTTP, целое число:
* 500 — ошибка при выполнении операции;
* 400 — Bad Request (при нехватке полей);
* 200 — успех.
message — строка:
* Причина ошибки (если она была);
* Отправлено успешно;
* Если отправка успешна, дополнительно возвращается id вставленной записи. id — идентификатор, который был присвоен объекту при добавлении в базу данных. Примеры oтветов:
- { "status": 500, "message": "Ошибка подключения к базе данных","id": null}
- { "status": 200, "message": null, "id": 34 }
После того, как турист добавит в базу данных информацию о новом перевале, сотрудники ФСТР проведут модерацию для каждого нового объекта и поменяют поле status. Допустимые значения поля status:

* 'NW' — по-умолчанию, только созданный объект;
* 'PN' — модератор взял в работу;
* 'AC' — модерация прошла успешно;
* 'RJ' — модерация прошла, информация не принята.
### Метод:

`GET /submitData/<id>`
получает одну запись (перевал) по её id с выведением всей информацию об перевале, в том числе статус модерации.

### Метод:

`PATCH /submitData/<id>`
позволяет отредактировать существующую запись (замена), при условии что она в статусе "NW". При этом редактировать можно все поля, кроме тех, что содержат ФИО, адрес почты и номер телефона. В качестве результата изменения приходит ответ содержащий следующие данные:

state:
1 — если успешно удалось отредактировать запись в базе данных.
0 — в отредактировать запись не удалось.
message: сообщение о причине неудачного обновления записи.
### Метод:

`GET /submitData/?tourist_id__email=<email>`
позволяет получить данные всех объектов, отправленных на сервер пользователем с указанной почтой.

В качестве реализации использована фильтрация по адресу электронной почты пользователя с помощью пакета django-filter.   
