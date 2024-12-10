# Создание контейнера
```
docker build -t form_giver . 
```
или ```make build```
# Запуск контейнера
```
docker run -e DB_PATH="data/forms.json" -d --volume "./data/:/app/data/" -p5000:5000 form_giver 
```
или ```make run```

```DB_PATH``` - путь к базе данных (первый каталог должен соответствовать бинду /app/*)

# Тестирование
```
make test
```
Шаблон запроса
```
curl -X POST -d 'field1=value&field2=value' http://localhost:5000/get_form
```
