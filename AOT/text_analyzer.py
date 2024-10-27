import tkinter as tk
from tkinter import messagebox, filedialog
import spacy
import os  # Для открытия локального файла
from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer

# Загрузка предобученной модели spaCy для русского языка
nlp = spacy.load("ru_core_news_sm")

# Инициализация модели тонального анализа Dostoevsky один раз при старте программы
tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

# Функция для анализа текста
def analyze_text():
    text = text_entry.get("1.0", tk.END).strip()
    
    if not text:
        messagebox.showerror("Ошибка", "Пожалуйста, введите текст.")
        return

    # Лексико-грамматический и синтаксический анализ с помощью spaCy
    doc = nlp(text)
    lexicogrammar_output = []
    syntax_output = []
    for token in doc:
        lexicogrammar_output.append(f"{token.text}: {token.pos_} -> {token.head.text}")
        syntax_output.append(f"{token.text} ({token.dep_}) -> {token.head.text}")

    lexicogrammar_result = "\n".join(lexicogrammar_output)
    syntax_result = "\n".join(syntax_output)

    # Тональный анализ с помощью Dostoevsky
    sentiment = model.predict([text])[0]
    sentiment_result = "Тональный анализ:\n" + "\n".join([f"{key}: {value:.2f}" for key, value in sentiment.items()])

    # Функция для сохранения результата в текстовый файл
    def save_to_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Лексико-грамматический анализ:\n")
                f.write(lexicogrammar_result)
                f.write("\n\nСинтаксический анализ:\n")
                f.write(syntax_result)
                f.write("\n\n")
                f.write(sentiment_result)
            messagebox.showinfo("Успех", f"Результат сохранен в файл {file_path}")

    # Функция для открытия README
    def open_readme():
        readme_path = "README.md"  # Укажите правильный путь к вашему README файлу
        try:
            os.startfile(readme_path)  # Для Windows
        except AttributeError:
            os.system(f"open {readme_path}")  # Для MacOS
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")

    # Функция для закрытия обоих окон
    def close_both_windows():
        result_window.destroy()  # Закрываем окно с результатами
        root.quit()  # Закрываем главное окно и завершаем программу

    # Создание нового окна для вывода результата
    result_window = tk.Toplevel(root)
    result_window.title("Результаты анализа")

    result_text = tk.Text(result_window, wrap=tk.WORD, height=20, width=60)
    result_text.pack(pady=10, padx=10)

    result_text.insert(tk.END, "Лексико-грамматический анализ:\n")
    result_text.insert(tk.END, lexicogrammar_result)
    result_text.insert(tk.END, "\n\nСинтаксический анализ:\n")
    result_text.insert(tk.END, syntax_result)
    result_text.insert(tk.END, "\n\n")
    result_text.insert(tk.END, sentiment_result)

    # Добавление кнопки для сохранения результата
    save_button = tk.Button(result_window, text="Сохранить", command=save_to_file)
    save_button.pack(pady=10)

    # Добавление кнопки для открытия README
    open_readme_button = tk.Button(result_window, text="Открыть README", command=open_readme)
    open_readme_button.pack(pady=10)

    # Добавление кнопки для закрытия обоих окон
    close_button = tk.Button(result_window, text="Закрыть", command=close_both_windows)
    close_button.pack(pady=10)

# Создание основного окна программы
root = tk.Tk()
root.title("Анализ текста")

# Метка для ввода текста
text_label = tk.Label(root, text="Введите текст для анализа:")
text_label.pack(pady=10)

# Поле для ввода текста
text_entry = tk.Text(root, wrap=tk.WORD, height=10, width=60)
text_entry.pack(pady=10)

# Кнопка для запуска анализа
analyze_button = tk.Button(root, text="Анализировать текст", command=analyze_text)
analyze_button.pack(pady=10)

# Запуск основного цикла обработки событий
root.mainloop()
