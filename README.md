# api_yamdb

# Проект, который собирает отзывы пользователей на произведения.

## Описание

### Произведения делятся на категории: «Книги», «Фильмы», «Музыка» (возможно расширение списка админом).

### Сами произведения в проекте не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

### В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.

### Произведению может быть присвоен жанр «Сказка», «Рок» или «Артхаус» (возможно расширение списка админом).

### Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

### Реализована аутентификация по токену.

## Как установить проект

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AKafer/api_yamdb.git
cd api_yamdb
```

### Создать и активировать виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Выполнить миграции:

```
cd api_yamdb
python manage.py migrate
```

### Запустить проект:

```
python manage.py runserver
```

## Примеры

### Когда вы запустите проект, по адресу [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) будет доступна документация для API YaMDb. В документации описаны примеры работы API. Документация представлена в формате Redoc.

## Стек технологий

### Python 3, Django 2.2, Django REST framework, SQLite3, Simple-JWT

## Авторы проекта

### Сергей Сторожук - часть управления пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения через e-mail.

### Илья Лукичев - категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них.

### Екатерина Ежова - отзывы (Review) и комментарии (Comments): модели, представления, эндпойнты, права доступа для запросов, рейтинги произведений.

