import tkinter as tk
from tkinter import scrolledtext, messagebox
import sqlite3
from nltk.corpus import wordnet
import nltk
import webbrowser
import os
import subprocess

# Загружаем WordNet
nltk.download('wordnet')
nltk.download('omw-1.4')

class SearchEngineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Векторный поиск с WordNet")
        self.root.geometry("800x600")

        # Создаем базу данных и таблицу, если их нет
        self.create_database()

        # Интерфейс
        self.create_widgets()

    def create_database(self):
        """Создает базу данных и таблицу, если их нет."""
        self.conn = sqlite3.connect('documents.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        # Добавляем тестовые данные, если таблица пуста
        self.cursor.execute("SELECT COUNT(*) FROM documents")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.executemany('''
                INSERT INTO documents (title, content) VALUES (?, ?)
            ''', [
                ("Документ 1", "The cat is on the mat."),
                ("Документ 2", "A kitten is playing with a ball."),
                ("Документ 3", "The dog is barking loudly."),
            ])
            self.conn.commit()

    def create_widgets(self):
        """Создает элементы интерфейса."""
        # Поле для ввода текста
        self.input_label = tk.Label(self.root, text="Введите текст для поиска:")
        self.input_label.pack(pady=10)

        self.input_text = tk.Entry(self.root, width=80)
        self.input_text.pack(pady=10)

        # Кнопка поиска
        self.search_button = tk.Button(self.root, text="Поиск", command=self.perform_search)
        self.search_button.pack(pady=10)

        # Область для вывода результатов
        self.result_label = tk.Label(self.root, text="Результаты поиска:")
        self.result_label.pack(pady=10)

        self.result_area = scrolledtext.ScrolledText(self.root, width=100, height=20)
        self.result_area.pack(pady=10)

        # Кнопка помощи
        self.help_button = tk.Button(self.root, text="Помощь", command=self.show_help)
        self.help_button.pack(pady=10)

        # Кнопка отчета
        self.report_button = tk.Button(self.root, text="Отчет", command=self.show_report)
        self.report_button.pack(pady=10)

    def perform_search(self):
        """Выполняет поиск документов по введенному тексту."""
        query = self.input_text.get().strip()
        if not query:
            messagebox.showwarning("Ошибка", "Введите текст для поиска.")
            return

        # Очищаем область результатов
        self.result_area.delete(1.0, tk.END)

        # Получаем документы из базы данных
        self.cursor.execute("SELECT title, content FROM documents")
        documents = self.cursor.fetchall()

        # Ищем документы с похожими фрагментами
        results = []
        for title, content in documents:
            similarity = self.calculate_similarity(query, content)
            if similarity > 0.5:  # Порог схожести
                results.append((title, content, similarity))

        # Выводим результаты
        if not results:
            self.result_area.insert(tk.END, "Ничего не найдено.\n")
        else:
            for title, content, similarity in results:
                self.result_area.insert(tk.END, f"Документ: {title}\n")
                self.result_area.insert(tk.END, f"Содержимое: {content}\n")
                self.result_area.insert(tk.END, f"Схожесть: {similarity:.2f}\n\n")

    def calculate_similarity(self, query, content):
        """Вычисляет схожесть между запросом и текстом документа."""
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())

        # Используем WordNet для вычисления схожести
        similarity_score = 0
        for q_word in query_words:
            for c_word in content_words:
                synsets1 = wordnet.synsets(q_word)
                synsets2 = wordnet.synsets(c_word)
                if synsets1 and synsets2:
                    similarity = synsets1[0].wup_similarity(synsets2[0])
                    if similarity:
                        similarity_score += similarity

        return similarity_score / len(query_words) if query_words else 0

    def show_help(self):
        """Выводит руководство пользователя."""
        help_text = """
        Руководство пользователя:
        1. Введите текст в поле для ввода.
        2. Нажмите кнопку "Поиск", чтобы найти документы.
        3. Результаты поиска появятся в области ниже.
        4. Используйте кнопку "Помощь" для вывода этого руководства.
        5. Используйте кнопку "Отчет" для открытия файла README.md.
        """
        messagebox.showinfo("Помощь", help_text)

    def show_report(self):
        readme_path = "README.md"  # Укажите правильный путь к вашему README файлу
        try:
            os.startfile(readme_path)  # Для Windows
        except AttributeError:
            os.system(f"open {readme_path}")  # Для MacOS
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")




    def __del__(self):
        """Закрывает соединение с базой данных при завершении."""
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchEngineApp(root)
    root.mainloop()