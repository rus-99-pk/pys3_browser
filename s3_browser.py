import os  # Для работы с файловой системой / For file system operations
import tkinter as tk  # Библиотека для создания GUI / Library for GUI creation
from tkinter import ttk, messagebox, filedialog  # Дополнительные модули tkinter / Additional tkinter modules
import boto3  # Библиотека для работы с S3 / Library for S3 operations
from botocore.exceptions import ClientError  # Исключения для обработки ошибок S3 / Exceptions for S3 error handling
from botocore.config import Config  # Конфигурация для boto3 / Configuration for boto3

class S3Browser:
    def __init__(self, root):
        # Инициализация основного окна приложения / Initialize the main application window
        self.root = root
        self.root.title("Universal S3 Browser")  # Заголовок окна / Window title
        self.root.geometry("900x700")  # Размер окна / Window size

        # Переменные для подключения к S3 / Variables for S3 connection
        self.s3_client = None  # Клиент S3, изначально не инициализирован / S3 client, initially None
        self.endpoint_url = tk.StringVar()  # URL конечной точки / Endpoint URL
        self.access_key = tk.StringVar()  # Ключ доступа / Access key
        self.secret_key = tk.StringVar()  # Секретный ключ / Secret key
        
        self.create_widgets()  # Создание элементов интерфейса / Create UI elements

    def create_widgets(self):
        # Фрейм для настроек подключения / Frame for connection settings
        self.config_frame = ttk.LabelFrame(self.root, text="Connection Settings")
        self.config_frame.pack(fill="x", padx=10, pady=5)

        # Поле для ввода URL конечной точки / Endpoint URL input field
        ttk.Label(self.config_frame, text="Endpoint URL:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.config_frame, textvariable=self.endpoint_url, width=50).grid(row=0, column=1, padx=5, pady=5)

        # Поле для ввода ключа доступа / Access key input field
        ttk.Label(self.config_frame, text="Access Key:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.config_frame, textvariable=self.access_key, width=50).grid(row=1, column=1, padx=5, pady=5)

        # Поле для ввода секретного ключа / Secret key input field
        ttk.Label(self.config_frame, text="Secret Key:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.config_frame, textvariable=self.secret_key, width=50, show="*").grid(row=2, column=1, padx=5, pady=5)

        # Кнопка для подключения / Connect button
        ttk.Button(self.config_frame, text="Connect", command=self.connect_to_s3).grid(row=3, column=1, pady=10)

        # Фрейм для списка бакетов / Frame for bucket list
        self.bucket_frame = ttk.LabelFrame(self.root, text="Buckets")
        self.bucket_frame.pack(fill="x", padx=10, pady=5)

        # Список бакетов / Bucket listbox
        self.bucket_listbox = tk.Listbox(self.bucket_frame, height=10)
        self.bucket_listbox.pack(fill="x", padx=5, pady=5)
        self.bucket_listbox.bind('<<ListboxSelect>>', self.load_objects)  # Привязка события выбора / Bind selection event
        
        # Контекстное меню для бакетов / Context menu for buckets
        self.bucket_menu = tk.Menu(self.root, tearoff=0)
        self.bucket_menu.add_command(label="Copy bucket name", command=self.copy_bucket_name)
        self.bucket_listbox.bind("<Button-3>", self.show_bucket_menu)

        # Кнопка обновления списка бакетов / Refresh buckets button
        self.refresh_button = ttk.Button(self.bucket_frame, text="Refresh Buckets", command=self.load_buckets)
        self.refresh_button.pack(pady=5)

        # Фрейм для списка объектов / Frame for object list
        self.object_frame = ttk.LabelFrame(self.root, text="Objects")
        self.object_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Таблица для отображения объектов / Treeview for displaying objects
        self.object_tree = ttk.Treeview(self.object_frame, columns=("Name", "Size", "Last Modified"), show="headings")
        self.object_tree.heading("Name", text="Name")  # Заголовок столбца имени / Name column header
        self.object_tree.heading("Size", text="Size (bytes)")  # Заголовок столбца размера / Size column header
        self.object_tree.heading("Last Modified", text="Last Modified")  # Заголовок столбца даты / Date column header
        self.object_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Контекстное меню для объектов / Context menu for objects
        self.object_menu = tk.Menu(self.root, tearoff=0)
        self.object_menu.add_command(label="Copy object path", command=self.copy_object_path)
        self.object_tree.bind("<Button-3>", self.show_object_menu)

        # Кнопка для скачивания выбранного объекта / Download selected object button
        self.download_button = ttk.Button(self.root, text="Download Selected", command=self.download_object)
        self.download_button.pack(pady=5)

    def show_bucket_menu(self, event):
        # Показать контекстное меню для бакетов / Show context menu for buckets
        self.bucket_menu.post(event.x_root, event.y_root)

    def show_object_menu(self, event):
        # Показать контекстное меню для объектов / Show context menu for objects
        self.object_menu.post(event.x_root, event.y_root)

    def copy_bucket_name(self):
        # Копировать имя выбранного бакета / Copy selected bucket name
        selected = self.bucket_listbox.curselection()
        if selected:
            bucket_name = self.bucket_listbox.get(selected)
            self.root.clipboard_clear()
            self.root.clipboard_append(bucket_name)
            messagebox.showinfo("Copied", "Bucket name copied to clipboard")

    def copy_object_path(self):
        # Копировать путь выбранного объекта / Copy selected object path
        selected_item = self.object_tree.selection()
        if selected_item:
            object_path = self.object_tree.item(selected_item)['values'][0]
            self.root.clipboard_clear()
            self.root.clipboard_append(object_path)
            messagebox.showinfo("Copied", "Object path copied to clipboard")

    def log_and_show_error(self, title, message):
        # Логировать и показать ошибку / Log and show error
        print(f"ERROR [{title}]: {message}")  # Вывод в терминал / Output to terminal
        messagebox.showerror(title, message)

    def connect_to_s3(self):
        # Подключение к S3 с использованием введенных данных / Connect to S3 using provided data
        endpoint = self.endpoint_url.get().strip()  # Получение URL / Get endpoint URL
        access_key = self.access_key.get().strip()  # Получение ключа доступа / Get access key
        secret_key = self.secret_key.get().strip()  # Получение секретного ключа / Get secret key

        # Проверка заполненности полей / Check if fields are filled
        if not endpoint or not access_key or not secret_key:
            messagebox.showwarning("Warning", "Please fill in all connection fields.")
            return

        try:
            # Создание клиента S3 / Create S3 client
            self.s3_client = boto3.client(
                's3',
                endpoint_url=endpoint,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                config=Config(signature_version='s3v4', s3={'addressing_style': 'path'})  # Используем стиль пути / Use path style
            )
            # Проверка подключения путем запроса списка бакетов / Verify connection by requesting bucket list
            self.s3_client.list_buckets()
            self.load_buckets()  # Загрузка бакетов после успешного подключения / Load buckets after successful connection
            messagebox.showinfo("Success", "Connected successfully!")  # Сообщение об успешном подключении / Success message
        except ClientError as e:
            # Обработка ошибок клиента S3 / Handle S3 client errors
            self.log_and_show_error("Error", f"Client error during connection: {str(e)}")
            self.s3_client = None  # Сброс клиента при ошибке / Reset client on error
        except Exception as e:
            # Обработка непредвиденных ошибок / Handle unexpected errors
            self.log_and_show_error("Error", f"Unexpected error during connection: {str(e)}")
            self.s3_client = None  # Сброс клиента при ошибке / Reset client on error

    def load_buckets(self):
        # Загрузка списка бакетов / Load list of buckets
        if not self.s3_client:
            messagebox.showwarning("Warning", "Please connect to an S3 service first.")
            return

        self.bucket_listbox.delete(0, tk.END)  # Очистка списка / Clear the list
        try:
            response = self.s3_client.list_buckets()  # Запрос списка бакетов / Request bucket list
            print(f"Response from list_buckets: {response}")  # Логирование ответа для отладки / Log response for debugging
            if 'Buckets' not in response:
                # Проверка наличия ключа 'Buckets' в ответе / Check if 'Buckets' key is in response
                self.log_and_show_error("Error", "Server response does not contain 'Buckets' key.")
                return
            for bucket in response['Buckets']:
                self.bucket_listbox.insert(tk.END, bucket['Name'])  # Добавление бакетов в список / Add buckets to list
        except ClientError as e:
            self.log_and_show_error("Error", f"Client error loading buckets: {str(e)}")
        except Exception as e:
            self.log_and_show_error("Error", f"Unexpected error loading buckets: {str(e)}")

    def load_objects(self, event):
        # Загрузка объектов из выбранного бакета / Load objects from selected bucket
        if not self.s3_client:
            return

        self.object_tree.delete(*self.object_tree.get_children())  # Очистка таблицы / Clear the table
        selected_bucket = self.bucket_listbox.get(self.bucket_listbox.curselection())  # Получение выбранного бакета / Get selected bucket
        if not selected_bucket:
            return

        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')  # Пагинация для больших бакетов / Pagination for large buckets
            for page in paginator.paginate(Bucket=selected_bucket):
                if 'Contents' not in page:
                    continue
                for obj in page['Contents']:
                    # Добавление объекта в таблицу / Add object to table
                    self.object_tree.insert("", "end", values=(
                        obj['Key'],  # Имя объекта / Object key
                        obj['Size'],  # Размер объекта / Object size
                        obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S')  # Дата изменения / Last modified date
                    ))
        except ClientError as e:
            self.log_and_show_error("Error", f"Failed to load objects: {str(e)}")

    def download_object(self):
        # Скачивание выбранного объекта / Download selected object
        if not self.s3_client:
            messagebox.showwarning("Warning", "Please connect to an S3 service first.")
            return

        selected_bucket = self.bucket_listbox.get(self.bucket_listbox.curselection())  # Выбранный бакет / Selected bucket
        selected_item = self.object_tree.selection()  # Выбранный объект / Selected object
        if not selected_bucket or not selected_item:
            messagebox.showwarning("Warning", "Please select a bucket and an object.")
            return

        key = self.object_tree.item(selected_item)['values'][0]  # Имя объекта / Object key
        save_path = filedialog.asksaveasfilename(initialfile=key.split('/')[-1])  # Путь для сохранения / Save path
        if not save_path:
            return

        try:
            self.s3_client.download_file(selected_bucket, key, save_path)  # Скачивание файла / Download file
            messagebox.showinfo("Success", f"File downloaded to {save_path}")
        except ClientError as e:
            self.log_and_show_error("Error", f"Failed to download file: {str(e)}")

if __name__ == "__main__":
    # Запуск приложения / Run the application
    root = tk.Tk()
    app = S3Browser(root)
    root.mainloop()