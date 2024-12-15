# Глоссарий терминов (gRPC API)

Проект представляет собой сервис управления глоссарием терминов, реализованный с использованием gRPC. Сервис позволяет создавать, читать, обновлять и удалять термины, а также осуществлять поиск по ним.

## Функциональность

- Создание новых терминов
- Получение списка всех терминов с пагинацией
- Получение термина по названию
- Обновление описания термина
- Удаление термина
- Поиск терминов по части названия (streaming API)

## Технологический стек

- Python 3.9
- gRPC
- SQLAlchemy (ORM)
- SQLite (база данных)
- Protocol Buffers
- Docker

## Установка и запуск

### Локальный запуск

1. Создайте виртуальное окружение и активируйте его: 

```bash
python -m venv venv
source venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Сгенерируйте код из proto-файлов:

```bash
python3 -m grpc_tools.protoc \
-I./proto \
--python_out=./generated \
--grpc_python_out=./generated \
proto/glossary.proto
```

4. Запустите сервер:

```bash
python server/main.py
```

### Запуск через Docker

```bash
docker compose up --build
```

## Использование

### Python-клиент

Запустите тестовый клиент:

```bash
python client/main.py
```

### Использование grpcurl

1. Установите grpcurl:

```bash
brew install grpcurl
```

2. Примеры команд:

1. Получить список методов

```bash
grpcurl -plaintext localhost:50051 list
```

2. Создать термин

```bash
grpcurl -plaintext -d '{
"term": "Docker",
"description": "Платформа для контейнеризации приложений"
}' localhost:50051 glossary.GlossaryService/CreateTerm
```

3. Получить список терминов

```bash
grpcurl -plaintext -d '{
"skip": 0,
"limit": 10
}' localhost:50051 glossary.GlossaryService/ListTerms
```

4. Поиск терминов

```bash
grpcurl -plaintext -d '{
"query": "Docker"
}' localhost:50051 glossary.GlossaryService/SearchTerms
```

## API методы

1. `ListTerms`: Получение списка терминов с пагинацией
2. `GetTerm`: Получение термина по названию
3. `CreateTerm`: Создание нового термина
4. `UpdateTerm`: Обновление существующего термина
5. `DeleteTerm`: Удаление термина
6. `SearchTerms`: Поиск терминов (streaming)

## Обработка ошибок

Сервис возвращает следующие коды ошибок:
- `NOT_FOUND`: Термин не найден
- `ALREADY_EXISTS`: Термин уже существует
- `INVALID_ARGUMENT`: Некорректные параметры запроса

## Разработка

Для внесения изменений в API:
1. Измените proto/glossary.proto
2. Перегенерируйте код:

```bash
python -m grpc_tools.protoc -I./proto --python_out=./generated --grpc_python_out=./generated proto/glossary.proto
```
3. Обновите реализацию в server/service.py