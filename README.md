# makers online course

## Информация о файлах конфигурации
Все конфигурции можно найти в директории:
```bash
src/makers/config
```

## Информаци о ENV-параметрах
Имеющиеся env-параметры в проекте:
```
POSTGRES_SERVER: str
POSTGRES_USER: str
POSTGRES_PASSWORD: str
POSTGRES_DB: str
```

### Запуск воркера

1. Создайте виртуальное окружение

```bash
python3 -m venv venv
```

2. Активировать виртуальное окружение: 

```bash
source venv/bin/activate
```

3. Установить зависимости: 

```bash
pip3 install -r requirements.txt
```

4. Собрать приложение как модуль:

```bash
python3 -m pip install .
```

5. Запусить приложение:
```bash
makers
```

