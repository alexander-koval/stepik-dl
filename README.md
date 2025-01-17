# Stepik Course Content Fetcher

Этот скрипт предназначен для извлечения контента курсов с сайта Stepik и конвертации его в различные форматы с использованием Pandoc.

## Требования

Перед использованием скрипта убедитесь, что у вас установлены следующие компоненты:

- Python 3.x
- [Poetry](https://python-poetry.org/)
- [Google Chrome](https://www.google.com/chrome/) или [Chromium](https://www.chromium.org/)
- Правильная версия [ChromeDriver](https://sites.google.com/chromium.org/driver/), соответствующая вашей версии браузера

## Установка

1. **Клонируйте репозиторий**:

   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```

2. **Убедитесь, что Poetry установлен**:

   Если у вас еще не установлен Poetry, следуйте [инструкциям по установке](https://python-poetry.org/docs/#installation).

3. **Установите зависимости**:

   Установите все зависимости, указанные в `pyproject.toml`, с помощью команды:

   ```bash
   poetry install
   ```

4. **Убедитесь, что Pandoc установлен**:

   Вы можете установить его через менеджер пакетов вашей ОС или скачать с [официального сайта](https://pandoc.org/installing.html).

## Использование

Запустите скрипт с использованием `poetry run` следующим образом:

```bash
poetry run python script.py <url> --sessionid <sessionid> --chromedriver-path <chromedriver_path> --chromium-path <chromium_path> --format <output_format> [-o <output_file>] [--output-dir <output_directory>]
```

### Параметры:

- `<url>`: URL страницы курса Stepik, которую вы хотите извлечь.
- `--sessionid`: Ваш ID сессии Stepik. Вы можете получить его из cookies вашего браузера после входа на сайт Stepik.
- `--chromedriver-path`: Путь к исполняемому файлу ChromeDriver.
- `--chromium-path`: Путь к исполняемому файлу Chromium.
- `--format`: Желаемый формат вывода. Поддерживаются следующие форматы:
  - `org`: Emacs Org Mode
  - `markdown`: Markdown формат
  - `html`: HTML документ
  - `pdf`: PDF документ (требуется LaTeX)
  - `docx`: MS Word документ
  - `rst`: reStructuredText
- `-o, --output`: (необязательно) Имя для выходного файла. Если не задано, используется имя по умолчанию `stepik_content.<output_format>`.
- `--output-dir`: (необязательно) Директория для сохранения выходного файла. По умолчанию используется текущая директория (`.`).

### Пример:

```bash
poetry run python script.py "https://stepik.org/example-course" --sessionid "your_session_id" --chromedriver-path "/path/to/chromedriver" --chromium-path "/path/to/chromium" --format markdown -o my_course.md --output-dir /path/to/save
```

## Замечания

- Убедитесь, что у вас есть соответствующие права доступа для чтения файлов `chromedriver` и `chromium`.
- Для создания PDF может потребоваться установка дополнительного программного обеспечения, такого как LaTeX.
- Долгий загрузочный процесс может быть вызван сложностью / объемом контента курса на Stepik. Направляйте ожидания на время конвертации.