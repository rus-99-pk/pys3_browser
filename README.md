# Universal S3 Browser

## Описание / Description

**Русский**:
Universal S3 Browser — это кроссплатформенное приложение с графическим интерфейсом (GUI), написанное на Python 3, для работы с S3-совместимыми хранилищами, такими как AWS S3, MinIO, Wasabi и другими. Оно позволяет подключаться к любому S3-сервису, просматривать список бакетов, загружать объекты и скачивать файлы, указывая параметры подключения непосредственно в интерфейсе.

***English**:
Universal S3 Browser is a cross-platform GUI application written in Python 3 for interacting with S3-compatible storage services like AWS S3, MinIO, Wasabi, and others. It enables users to connect to any S3 service, view a list of buckets, browse objects, and download files by specifying connection details directly in the interface.*

---

## Возможности / Features

- **Поддержка любых S3-совместимых сервисов** / Support for any S3-compatible service
- **Гибкое подключение через GUI** / Flexible GUI-based connection
- **Просмотр бакетов и объектов** / View buckets and objects
- **Скачивание файлов** / File downloading
- **Кроссплатформенность (Windows, macOS, Linux)** / Cross-platform (Windows, macOS, Linux)

---

## Скриншот интерфейса / GUI Screen
![изображение](https://github.com/user-attachments/assets/a1f9e5a3-11d3-48ed-a9ac-4f37eeae4ebe)

---

## Установка / Installation

### Требования / Requirements
- Python 3.8+
- Установленные библиотеки: `boto3`, `tkinter`

### Шаги / Steps

1. **Установите Python**:
   Скачайте и установите Python 3 с официального сайта / *Download and install Python 3 from the [official website](https://www.python.org/downloads/).*.

2. **Установите зависимости**:
   
   Откройте терминал и выполните:
   ```bash
   pip install boto3
   ```

   **Примечание**: `tkinter` обычно предустановлен с Python. Если его нет:
   - На Ubuntu/Debian: `sudo apt-get install python3-tk`
   - На macOS: `brew install python-tk` (через Homebrew)
   - На Windows: обычно не требуется.
 
   ***Note:** `tkinter` is usually bundled with Python. If missing:*
   - *Ubuntu/Debian: `sudo apt-get install python3-tk`*
   - *macOS: `brew install python-tk` (via Homebrew)*
   - *Windows: typically not required.*

3. **Скачайте код**:
   Склонируйте репозиторий или скачайте файл `s3_browser.py`.
   *Clone the repository or download the `s3_browser.py` file.*

---

## Использование / Usage

1. **Запустите приложение**:
   В терминале выполните:
   ```bash
   python3 s3_browser.py
   ```
   *Run in terminal:*
   ```bash
   python3 s3_browser.py
   ```

2. **Настройте подключение**:
   - **Endpoint URL**: Укажите адрес вашего S3-сервиса (например, `http://s3.test.ru:9000`).
   - **Access Key**: Введите ключ доступа.
   - **Secret Key**: Введите секретный ключ.
   - Нажмите кнопку **Connect**.

   ***Configure connection:***
    - ***Endpoint URL**: Enter your S3 service address (e.g., `http://s3.test.ru:9000`).*
    - ***Access Key**: Enter your access key.*
    - ***Secret Key**: Enter your secret key.*
    - *Click **Connect**.*

3. **Работа с данными**:
   - Выберите бакет из списка для просмотра объектов.
   - Выберите объект и нажмите **Download Selected** для скачивания.
   - Используйте **Refresh Buckets** для обновления списка бакетов.

   ***Work with data:***
   - *Select a bucket from the list to view objects.*
   - *Select an object and click **Download Selected** to download.*
   - *Use **Refresh Buckets** to update the bucket list.*

---

## Примеры подключения / Connection Examples

- **AWS S3**:
  - Endpoint: `https://s3.amazonaws.com`
  - Access Key: `<ваш ключ>` / `<your key>`
  - Secret Key: `<ваш секрет>` / `<your secret>`

- **MinIO**:
  - Endpoint: `http://localhost:9000`
  - Access Key: `minioadmin` (по умолчанию / default)
  - Secret Key: `minioadmin` (по умолчанию / default)

- **Custom S3**:
  - Endpoint: `http://s3.test.ru:9000`
  - Access Key: `<ваш ключ>` / `<your key>`
  - Secret Key: `<ваш секрет>` / `<your secret>`

---

## Устранение неполадок / Troubleshooting

- **Ошибка "Invalid endpoint"**: Убедитесь, что вы указали полный URL с протоколом (`http://` или `https://`) и портом, если требуется.
  ***Error "Invalid endpoint"**: Ensure you’ve provided a full URL with protocol (`http://` or `https://`) and port if needed.*

- **Ошибка "Buckets"**: Если сервер не поддерживает `list_buckets()`, уточните у администратора имя бакета и добавьте его вручную в код.
  ***Error "Buckets"**: If the server doesn’t support `list_buckets()`, check with your admin for a bucket name and add it manually to the code.*

- **Нет подключения**: Проверьте правильность учетных данных и доступность сервера.
  ***No connection**: Verify credentials and server availability.*

---

## Автор / Author

https://t.me/rus_99_pk

---

## Лицензия / License

MIT License — используйте, модифицируйте и распространяйте свободно!
*MIT License — feel free to use, modify, and distribute!*
