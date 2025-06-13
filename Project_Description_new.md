<div style="font: bold normal 110% sans-serif; color: #8A2BE2; border-bottom: 5px double #8A2BE2; background-color:#2A0B52; padding: 5px;"></div>   

# <a id="s1"><font color="green">1. Описание проекта</font></a>  
"Community Pulse" — это интерактивная платформа, где анонимные пользователи могут создавать вопросы на 
общественно значимые темы и получать мнения других участников. Эта система позволяет участникам выражать 
свое согласие или несогласие по различным вопросам и видеть общую статистику мнений, что делает ее 
отличным инструментом для измерения общественного настроения по разнообразным темам.  
<div style="font: bold normal 110% sans-serif; color: #8A2BE2; white-space: pre; border-top: 2px dotted #008000; padding: 5px;"></div>  

### <a id="s6" style="color: #008000">ПЕРЕД запуском приложения в терминале</a>    

1. Инициализировать и применить миграции или УДАЛИТЬ старые (папки "migrations" 
вместе с папкой БД "instance"), если они есть, и заново их создать:
```
flask db init
flask db migrate
flask db upgrade
```
2. И только ПОТОМ запускать приложение:
```
python run.py
```
3. В файле <a>http.http</a> выбрать ЗАПРОС на получение списка вопросов и выполнить его.  
4. Перейти по адресу (добавить эндпоинт /questions):  http://127.0.0.1:5000/questions/.  
Должен появиться JSON:  

<img src="other/figs/img.png" width="350" alt=""/>

<a id="img1" style="margin: 40px; color:#808080;">Fig. 1 - Код приложения: app.js, часть 1.</a>

4. В файле <a>http.http</a> выполнить запросы на СОЗДАНИЕ юзеров, вопросов и ответов на них.  
<div style="font: bold normal 110% sans-serif; color: #8A2BE2; white-space: pre; border-top: 2px dotted #008000; padding: 5px;"></div>  



# <a id="s2"><font color="green">2. Базовый код проекта: модели Questions, Responses</font></a>  
См. Video от 10.06.2025: Python Advanced 4: Flask: Summary session 1, 53:40.
<div style="font: bold normal 110% sans-serif; color: #8A2BE2; white-space: pre; border-top: 2px dotted #008000; padding: 5px;"></div>  



# <a id="s3"><font color="green">3. Модель User</font></a>  
См. Video от 10.06.2025: Python Advanced 4: Flask: 
Summary session 1, __:__.
<div style="font: bold normal 110% sans-serif; color: #8A2BE2; white-space: pre; border-top: 2px dotted #008000; padding: 5px;"></div>  





# <a id="s4"><font color="green">4. Flask-проект - Домашнее задание 5</font></a>  
Цели задания: Расширить функциональность существующего API для поддержки категорий вопросов.
Задачи:
1. Создание модели Category:  
   - Создайте новую модель Category с использованием SQLAlchemy в модуле models.
   - Модель должна содержать следующие поля:
     - id: первичный ключ, целое число, авто-инкремент.
     - name: строка, название категории, не должно быть пустым.
   - Модель Question должна быть обновлена, чтобы включить ссылку на Category 
   через внешний ключ.
2. Миграция базы данных:
   - Создайте новую миграцию для добавления таблицы категорий и обновления таблицы вопросов 
   с использованием Flask-Migrate.
<div style="font: bold normal 110% sans-serif; color: #8A2BE2; white-space: pre; border-top: 2px dotted #008000; padding: 5px;"></div>  



# <a id="s5"><font color="green">5. Flask-проект - Домашнее задание 6</font></a>  
Цели задания: Расширить функциональность существующего API для поддержки категорий вопросов.
Задачи: 
1. Обновление схем Pydantic:  
   - Добавьте новую схему CategoryBase в schemas/question.py для сериализации и 
   валидации данных категории.
   - Обновите схему QuestionCreate и QuestionResponse для интеграции данных о категории.
2. Разработка API эндпоинтов:  
   - Создайте новые эндпоинты для создания, чтения, обновления и удаления категорий.
     - POST /categories: создание новой категории.
     - GET /categories: получение списка всех категорий.
     - PUT /categories/{id}: обновление категории по ID.
     - DELETE /categories/{id}: удаление категории по ID.
   - Обновите существующие эндпоинты вопросов, чтобы они поддерживали работу с категориями.
     - GET /questions: должен возвращать вопросы с информацией о категориях.
     - POST /questions: должен позволять указывать категорию при создании вопроса.
<div style="font: bold normal 110% sans-serif; color: #8A2BE2; white-space: pre; border-top: 2px dotted #008000; padding: 5px;"></div>



### <a id="v1"><font color="green">Links on Videos</font></a>  

10.06.2025
Video: Python Advanced 4: Flask: Summary session 1 (Повторение, решение задач)    Müller Alexander
link: https://player.vimeo.com/video/1092111490?h=02293fbf54

11.06.2025
Video: Python Advanced 4: Flask: Summary session 1 (Повторение, решение задач)
link: https://player.vimeo.com/video/1092444197?h=4fc42a8cb4

11.06.2025
Video: Python Adv 8: Flask: Summary session 2 (Повторение, решение задач)
link: https://player.vimeo.com/video/1092439106?h=1ae131892c




---
<div style="font: bold normal 110% sans-serif; color: #8A2BE2; white-space: pre; border-top: 2px dotted #008000; padding: 5px;"></div>  


`pip list` - для просмотра установленных библиотек.  
`pip freeze > requirements.txt` - для импорта списка библиотек в *requirements.txt*.  
`pip install -r requirement.txt` - для установки в скаченном проекте необходимых библиотек.  

