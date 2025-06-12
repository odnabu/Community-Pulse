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


---
<div style="font: bold normal 110% sans-serif; color: #8A2BE2; white-space: pre; border-top: 2px dotted #008000; padding: 5px;"></div>  

