## Задание
https://drive.google.com/file/d/1nTTSmdbbJPnTCC3_Pi0oeIc5oFXFW0K2/view
## API
+ GET city/ - получить список городов и информацию о них;
+ GET city/id - получить инфомацию о городе по id;
+ GET city/id/street - получить список улиц в городе;
+ GET shop/ - получить список магазинов;
+ GET shop/?city=&street=&open=1/0 - получить список магазинов согласно уловиям;
+ POST shop/ - добавить город;
+ DELETE shop/id - удалить город по id;
## Запуск
перейти в директорию app и выполнить gunicorn app.wsgi:application.
Доступ к панели администратора: root 1234. В качестве базы данных sqlite.
  
